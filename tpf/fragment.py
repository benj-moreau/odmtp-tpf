from rdflib import Dataset, Namespace


class Fragment(object):

    HYDRA = Namespace("http://www.w3.org/ns/hydra/core#")
    VOID = Namespace("http://rdfs.org/ns/void#")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    DCTERMS = Namespace("http://purl.org/dc/terms/")

    def __init__(self):
        self.rdf_graph = Dataset()

    def add_data_triple(self, subject, predicate, obj):
        self.rdf_graph.add((subject, predicate, obj))

    def serialize(self):
        return self.rdf_graph.serialize(format="trig", encoding="utf-8")
