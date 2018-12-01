from utils.xr2rml_mapper import Xr2rmlMapper
from odmtp.modules.trimmer import Trimmer


class TrimmerXr2rmlTwitter(Trimmer):

    def __init__(self, extended=False):
        if extended:
            self.mapping = Xr2rmlMapper('./mapping/mapping_tweet.ttl', './ontologie/twitter_ontologie.ttl').get_mapping()
        else:
            self.mapping = Xr2rmlMapper('./mapping/mapping_tweet.ttl').get_mapping()
