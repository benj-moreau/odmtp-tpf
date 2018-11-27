from utils.xr2rml_mapper import Xr2rmlMapper
from odmtp.modules.trimmer import Trimmer


class TrimmerXr2rmllinkedin(Trimmer):

    def __init__(self):
        self.mapping = Xr2rmlMapper('./mapping/mapping_linkedin.ttl').get_mapping()
