from rdflib import URIRef


class Trimmer(object):

    def get_reduced_mapping(self, tpq):
        raise NotImplementedError()

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
