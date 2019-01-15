class Odmtp(object):

    def __init__(self, trimmer, tp2query, mapper):
        self.trimmer = trimmer
        self.tp2query = tp2query
        self.mapper = mapper

    def match(self, tpq, fragment, request, extended=False):
        reduced_mapping = self.trimmer.get_reduced_mapping(tpq)
        result_set = self.tp2query.request(tpq, reduced_mapping, fragment, request, extended)
        self.mapper.result_set_2_rdf(result_set, reduced_mapping, fragment)
