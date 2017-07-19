from rdflib import Graph, URIRef, Namespace, RDF

rr = Namespace("http://www.w3.org/ns/r2rml#")
rml = Namespace("http://semweb.mmlab.be/ns/rml#")
xrr = Namespace("http://www.i3s.unice.fr/ns/xr2rml#")


class Xr2rmlMapper(object):
    """This class partialy implements the XR2RML mapping langage."""

    def __init__(self, filename):
        self.mapping = Graph()
        self.preprocessed_mapping = Graph()
        with open(filename, 'r') as content_file:
            file_content = content_file.read()
        self.mapping.parse(format="turtle", data=file_content)
        self.logical_sources = {}
        self._preprocess_mapping()

    def get_mapping(self):
        return self.preprocessed_mapping

    def get_logical_sources(self):
        return self.logical_sources

    def print_pre_mapping(self):
        print self.logical_sources
        for s, p, o in self.preprocessed_mapping:
            print "s=%s" % s
            print "p=%s" % p
            print "o=%s" % o

    def _preprocess_mapping(self):
        resources = []
        for s in self.mapping.subjects():
            subject = None
            if isinstance(s, URIRef) and s not in resources:
                resources.append(s)
                for node in self.mapping.objects(subject=s, predicate=rr.subjectMap):
                    for template in self.mapping.objects(subject=node, predicate=rr.template):
                        subject = template
                        for type_class in self.mapping.objects(subject=node, predicate=rr['class']):
                            self.preprocessed_mapping.add((subject, RDF.type, type_class))
                for node in self.mapping.objects(subject=s, predicate=rr.predicateObjectMap):
                    predicate = None
                    for predicate_object in self.mapping.objects(subject=node, predicate=rr.predicate):
                        predicate = predicate_object
                        for object_map in self.mapping.objects(subject=node, predicate=rr.objectMap):
                            for reference in self.mapping.objects(subject=object_map, predicate=xrr.reference):
                                self.preprocessed_mapping.add((subject, predicate, reference))
                for node in self.mapping.objects(subject=s, predicate=xrr.logicalSource):
                    self.logical_sources[subject] = {}
                    for query in self.mapping.objects(subject=node, predicate=xrr.query):
                        self.logical_sources[subject]['query'] = query
                    for iterator in self.mapping.objects(subject=node, predicate=rml.iterator):
                        self.logical_sources[subject]['iterator'] = iterator
