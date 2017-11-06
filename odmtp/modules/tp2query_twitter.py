from rdflib import URIRef, Literal, Namespace, BNode, RDF, XSD
from urllib import urlencode
from urlparse import urlparse

from utils.twitter_api import TwitterApi
from odmtp.modules.tp2query import Tp2Query


TWEET_SEARCH = "search/tweets.json"
TWEET_LOOKUP = "statuses/show/%s.json"

# Associate key of the JSON result set with twitter query operators.
# see https://dev.twitter.com/rest/public/search
TWITTER_OPERATORS = {
    '$.text': '"%s"',
    '$.entities.hashtags.[*].text': '#%s',
    '$.entities.urls.[*].expanded_url': 'url:%s',
    '$.user.screen_name': 'from:%s'
}

BASE_QUERY = 'filter:safe'

TWEETS_PER_PAGE = 5

TPF_URL = '%s://%s/twitter/'

# twitter search API returns top 15000 tweets matching query
# So i set up a limit to count maximum number of result (TWEETS_PER_PAGE * LAST_PAGE)
LAST_PAGE = 5


class Tp2QueryTwitter(Tp2Query):

    def request(self, tpq, reduced_mapping, fragment, request):
        tpf_url = urlparse(request.build_absolute_uri())
        tpf_url = TPF_URL % (tpf_url.scheme, tpf_url.netloc)
        last_result = False
        result_set = None
        query_parameters = {}
        number_of_triples_per_tweets = len(reduced_mapping.mapping)
        twitter = TwitterApi()
        if 'access_token' not in request.COOKIES:
            request.COOKIES['access_token'] = twitter.get_access_token()
        twitter.set_access_token(request.COOKIES['access_token'])
        for subject_prefix in reduced_mapping.logical_sources:
            if tpq.subject is None or tpq.subject.startswith(subject_prefix):
                query_url = reduced_mapping.logical_sources[subject_prefix]['query']
        if tpq.subject:
            tweet_id = tpq.subject.rpartition('/')[2]
            query_url = "%s%s" % (query_url, TWEET_LOOKUP % tweet_id)
            result_set = twitter.request(query_url)
            result_set = [result_set]
            last_result = True
            total_nb_triples = len(result_set) * number_of_triples_per_tweets
        else:
            q = BASE_QUERY
            if tpq.obj:
                if tpq.predicate:
                    for s, p, o in reduced_mapping.mapping:
                        if '%s' % o in TWITTER_OPERATORS:
                            q = "%s %s" % (q, TWITTER_OPERATORS['%s' % o] % '%s' % tpq.obj)
                else:
                    q = "%s %s" % (q, '"%s"' % tpq.obj)
            query_parameters['q'] = q
            query_parameters['count'] = TWEETS_PER_PAGE
            query_url = "%s%s" % (query_url, TWEET_SEARCH)
            parameters = "?%s" % urlencode(query_parameters)
            for i in range(tpq.page):
                result_set = twitter.request("%s%s" % (query_url, parameters))
                if 'next_results' in result_set['search_metadata']:
                    parameters = result_set['search_metadata']['next_results']
                else:
                    last_result = True
                    break
            result_set = result_set['statuses']
            if tpq.page >= LAST_PAGE:
                last_result = True
            total_nb_triples = TWEETS_PER_PAGE * LAST_PAGE * number_of_triples_per_tweets
        nb_triple_per_page = TWEETS_PER_PAGE * number_of_triples_per_tweets
        self._frament_fill_meta(tpq, fragment, last_result, total_nb_triples, nb_triple_per_page, request, tpf_url)
        return result_set

    def _frament_fill_meta(self, tpq, fragment, last_result, total_nb_triples, nb_triple_per_page, request, tpf_url):
        meta_graph = self._tpf_uri(tpf_url, 'metadata')
        fragment.add_graph(meta_graph)
        dataset_base = self._tpf_uri(tpf_url)
        source = URIRef(request.build_absolute_uri())
        dataset_template = Literal('%s%s' % (dataset_base, '{?subject,predicate,object}'))
        data_graph = self._tpf_uri(tpf_url, 'dataset')
        tp_node = BNode('triplePattern')
        subject_node = BNode('subject')
        predicate_node = BNode('predicate')
        object_node = BNode('object')
        HYDRA = Namespace("http://www.w3.org/ns/hydra/core#")
        VOID = Namespace("http://rdfs.org/ns/void#")
        FOAF = Namespace("http://xmlns.com/foaf/0.1/")
        DCTERMS = Namespace("http://purl.org/dc/terms/")

        fragment.add_meta_quad(meta_graph, FOAF['primaryTopic'], dataset_base, meta_graph)
        fragment.add_meta_quad(data_graph, HYDRA['member'], data_graph, meta_graph)
        fragment.add_meta_quad(data_graph, RDF.type, VOID['Dataset'], meta_graph)
        fragment.add_meta_quad(data_graph, RDF.type, HYDRA['Collection'], meta_graph)
        fragment.add_meta_quad(data_graph, VOID['subset'], source, meta_graph)
        fragment.add_meta_quad(data_graph, VOID['uriLookupEndpoint'], dataset_template, meta_graph)
        fragment.add_meta_quad(data_graph, HYDRA['search'], tp_node, meta_graph)
        fragment.add_meta_quad(tp_node, HYDRA['template'], dataset_template, meta_graph)
        fragment.add_meta_quad(tp_node, HYDRA['variableRepresentation'], HYDRA['ExplicitRepresentation'], meta_graph)
        fragment.add_meta_quad(tp_node, HYDRA['mapping'], subject_node, meta_graph)
        fragment.add_meta_quad(tp_node, HYDRA['mapping'], predicate_node, meta_graph)
        fragment.add_meta_quad(tp_node, HYDRA['mapping'], object_node, meta_graph)
        fragment.add_meta_quad(subject_node, HYDRA['variable'], Literal("subject"), meta_graph)
        fragment.add_meta_quad(subject_node, HYDRA['property'], RDF.subject, meta_graph)
        fragment.add_meta_quad(predicate_node, HYDRA['variable'], Literal("predicate"), meta_graph)
        fragment.add_meta_quad(predicate_node, HYDRA['property'], RDF.predicate, meta_graph)
        fragment.add_meta_quad(object_node, HYDRA['variable'], Literal("object"), meta_graph)
        fragment.add_meta_quad(object_node, HYDRA['property'], RDF.object, meta_graph)

        fragment.add_meta_quad(dataset_base, VOID['subset'], source, meta_graph)
        fragment.add_meta_quad(source, RDF.type, HYDRA['PartialCollectionView'], meta_graph)
        fragment.add_meta_quad(source, DCTERMS['title'], Literal("TPF Twitter search API 1.1"), meta_graph)
        fragment.add_meta_quad(source, DCTERMS['description'], Literal("Triple Pattern from the twitter api matching the pattern {?s=%s, ?p=%s, ?o=%s}" % (tpq.subject, tpq.predicate, tpq.obj)), meta_graph)
        fragment.add_meta_quad(source, DCTERMS['source'], data_graph, meta_graph)
        fragment.add_meta_quad(source, HYDRA['totalItems'], Literal(total_nb_triples, datatype=XSD.int), meta_graph)
        fragment.add_meta_quad(source, VOID['triples'], Literal(total_nb_triples, datatype=XSD.int), meta_graph)
        fragment.add_meta_quad(source, HYDRA['itemsPerPage'], Literal(nb_triple_per_page, datatype=XSD.int), meta_graph)
        fragment.add_meta_quad(source, HYDRA['first'], self._tpf_url(dataset_base, 1, tpq.subject, tpq.predicate, tpq.obj), meta_graph)
        if tpq.page > 1:
            fragment.add_meta_quad(source, HYDRA['previous'], self._tpf_url(dataset_base, tpq.page - 1, tpq.subject, tpq.predicate, tpq.obj), meta_graph)
        if not last_result:
            fragment.add_meta_quad(source, HYDRA['next'], self._tpf_url(dataset_base, tpq.page + 1, tpq.subject, tpq.predicate, tpq.obj), meta_graph)
        fragment.add_prefix('twittertpf', Namespace("%s#" % tpf_url[:-1]))
        fragment.add_prefix('void', VOID)
        fragment.add_prefix('foaf', FOAF)
        fragment.add_prefix('hydra', HYDRA)
        fragment.add_prefix('purl', Namespace('http://purl.org/dc/terms/'))

    def _tpf_uri(self, tpf_url, tag=None):
        if tag is None:
            return URIRef(tpf_url)
        return URIRef("%s%s" % (tpf_url[:-1], '#%s' % tag))

    def _tpf_url(self, dataset_base, page, subject, predicate, obj):
        subject_parameter = subject if subject else ''
        predicate_parameter = predicate if predicate else ''
        object_parameter = ('"%s"^^%s' % (obj, obj._datatype)) if obj else ''
        parameters = {'page': page, 'subject': subject_parameter, 'predicate': predicate_parameter, 'object': object_parameter}
        return URIRef("%s?%s" % (dataset_base, urlencode(parameters)))
