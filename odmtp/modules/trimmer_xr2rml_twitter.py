from utils.xr2rml_mapper import Xr2rmlMapper
from odmtp.modules.trimmer import Trimmer
from rdflib import URIRef


class TrimmerXr2rmlTwitter(Trimmer):

    def get_reduced_mapping(self, tpq):
        xr2rml_mapping = Xr2rmlMapper('./mapping/mapping_tweet.ttl').get_mapping()
        self.mapping_triple_pattern_matching(xr2rml_mapping, tpq)
        return xr2rml_mapping

    def mapping_triple_pattern_matching(self, xr2rml_mapping, tpq):
        if tpq.predicate is not None:
            xr2rml_mapping.mapping = xr2rml_mapping.mapping & xr2rml_mapping.mapping.triples((None, tpq.predicate, None))
        if tpq.subject is not None:
            for s, p, o in xr2rml_mapping.mapping:
                subject_prefix = s.split('{')[0]
                if not tpq.subject.startswith(subject_prefix):
                    xr2rml_mapping.mapping.remove((s, p, o))
        if tpq.obj is not None and type(tpq.obj) is URIRef:
            object_prefix = s.split('{')[0]
            for s, p, o in xr2rml_mapping.mapping:
                if not tpq.obj.startswith(object_prefix):
                    xr2rml_mapping.mapping.remove((s, p, o))
