from utils.xr2rml_mapper import Xr2rmlMapper
from odmtp.modules.trimmer import Trimmer
from rdflib import URIRef


class TrimmerXr2rmlTwitter(Trimmer):

    def get_reduced_mapping(self, tpq):
        xr2rml_mapping = Xr2rmlMapper('./mapping/mapping_tweet.ttl').get_mapping()
        self.mapping_triple_pattern_matching(xr2rml_mapping, tpq)
        return xr2rml_mapping
