from utils.xr2rml_mapper import Xr2rmlMapper
from odmtp.modules.trimmer import Trimmer


class TrimmerXr2rmlTwitter(Trimmer):

    def __init__(self):
        self.mapping = Xr2rmlMapper('./mapping/mapping_tweet.ttl').get_mapping()
