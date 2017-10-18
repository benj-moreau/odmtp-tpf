class Xr2rmlMapping(object):
    """This class represents a xr2rml mapping."""

    def __init__(self, mapping_graph, logical_sources):
        self.mapping = mapping_graph
        self.logical_sources = logical_sources

    def mapping(self):
        return self.mapping

    def logical_sources(self):
        return self.logical_sources

    def print_mapping(self):
        print(self.logical_sources)
        for s, p, o in self.mapping:
            print("s=%s" % s)
            print("p=%s" % p)
            print("o=%s" % o)
