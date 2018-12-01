from utils.xr2rml_mapper import Xr2rmlMapper
from odmtp.modules.trimmer import Trimmer


class TrimmerXr2rmlGithub(Trimmer):

    def __init__(self, extended=False):
        if extended:
            self.mapping = Xr2rmlMapper('./mapping/mapping_github.ttl', './ontologie/github_ontologie.ttl').get_mapping()
        else:
            self.mapping = Xr2rmlMapper('./mapping/mapping_github.ttl').get_mapping()
