from utils.xr2rml_mapper import Xr2rmlMapper
from odmtp.modules.trimmer import Trimmer


class TrimmerXr2rmllinkedin(Trimmer):

    def __init__(self, extended=False):
        if extended:
            self.mapping = Xr2rmlMapper('./mapping/mapping_linkedin.ttl', './ontologie/linkedin_ontologie.ttl').get_mapping()
        else:
            self.mapping = Xr2rmlMapper('./mapping/mapping_linkedin.ttl').get_mapping()
