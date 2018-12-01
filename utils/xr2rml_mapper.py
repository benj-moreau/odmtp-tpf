from rdflib import Graph, URIRef, Namespace, RDF

from utils.xr2rml_mapping import Xr2rmlMapping
from utils.rml_closer import OWLLiteCloser

rr = Namespace("http://www.w3.org/ns/r2rml#")
rml = Namespace("http://semweb.mmlab.be/ns/rml#")
xrr = Namespace("http://www.i3s.unice.fr/ns/xr2rml#")


class Xr2rmlMapper(object):
    """This class partialy implements the XR2RML mapping langage."""

    def __init__(self, filename, ontology_filename=None):
        self.mapping = Graph()
        self.preprocessed_mapping = Graph()
        with open(filename, 'r') as content_file:
            file_content = content_file.read()
        self.mapping.parse(format="turtle", data=file_content)
        if ontology_filename:
            with open(ontology_filename, 'r') as content_file:
                ontology_content = content_file.read()
            ontology = Graph().parse(format="turtle", data=ontology_content)
            rml_closer = OWLLiteCloser()
            rml_closer.setOnto(ontology)
            rml_closer.setRML(self.mapping)
            rml_closer.enrich()
            self.mapping = rml_closer.rml
        self.logical_sources = {}
        self._preprocess_mapping()

    def get_mapping(self):
        return Xr2rmlMapping(self.preprocessed_mapping, self.logical_sources)

    def _preprocess_mapping(self):
        resources = {}
        for s in self.mapping.subjects():
            if isinstance(s, URIRef) and s not in resources:
                for node in self.mapping.objects(subject=s, predicate=rr.subjectMap):
                    for template in self.mapping.objects(subject=node, predicate=rr.template):
                        resources[s] = template
                        for type_class in self.mapping.objects(subject=node, predicate=rr['class']):
                            self.preprocessed_mapping.add((resources[s], RDF.type, type_class))
                for node in self.mapping.objects(subject=s, predicate=xrr.logicalSource):
                    subject_prefix = resources[s].split('{')[0]
                    self.logical_sources[subject_prefix] = {}
                    for query in self.mapping.objects(subject=node, predicate=xrr.query):
                        self.logical_sources[subject_prefix]['query'] = query
                    for iterator in self.mapping.objects(subject=node, predicate=rml.iterator):
                        self.logical_sources[subject_prefix]['iterator'] = iterator
        for s in resources:
            for node in self.mapping.objects(subject=s, predicate=rr.predicateObjectMap):
                predicate = None
                for predicate_object in self.mapping.objects(subject=node, predicate=rr.predicate):
                    predicate = predicate_object
                    for object_map in self.mapping.objects(subject=node, predicate=rr.objectMap):
                        for reference in self.mapping.objects(subject=object_map, predicate=xrr.reference):
                            self.preprocessed_mapping.add((resources[s], predicate, reference))
                        for parent in self.mapping.objects(subject=object_map, predicate=rr.parentTriplesMap):
                            if parent != resources[s]:
                                self.preprocessed_mapping.add((resources[s], predicate, resources[parent]))
