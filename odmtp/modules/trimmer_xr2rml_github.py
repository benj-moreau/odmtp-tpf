from utils.xr2rml_mapper import Xr2rmlMapper
from odmtp.modules.trimmer import Trimmer
# from rdflib import URIRef


class TrimmerXr2rmlGithub(Trimmer):

    def get_reduced_mapping(self, tpq):
        xr2rml_mapping = Xr2rmlMapper('./mapping/mapping_github.ttl').get_mapping()
        self.mapping_triple_pattern_matching(xr2rml_mapping, tpq)
        return xr2rml_mapping
