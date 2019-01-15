from rdflib import URIRef, Literal, Namespace, BNode, RDF, XSD
from urllib import urlencode
from urlparse import urlparse

from utils.github_api import GithubApi
from odmtp.modules.tp2query import Tp2Query


REPO_SEARCH = "search/repositories"
REPOS = "repositories"

# Associate key of the JSON result set with github query qualifiers.
# see https://help.github.com/articles/searching-repositories
GITHUB_QUALIFIERS = {
    '$.full_name': '%s in:full_name',
    '$.description': '%s in:description',
    '$.name': 'name:%s',
    '$.owner.login': 'user:%s',
    '$.created_at': 'created:%s',
    '$.updated_at': 'pushed:%s',
    '$.language': 'language:%s'
}

REPO_PER_PAGE = 5
TPF_URL = '%s://%s/github/%s'


class Tp2QueryGithub(Tp2Query):

    def request(self, tpq, reduced_mapping, fragment, request, extended):
        tpf_url = urlparse(request.build_absolute_uri())
        tpf_url = TPF_URL % (tpf_url.scheme, tpf_url.netloc, 'extended/') if extended else TPF_URL % (tpf_url.scheme, tpf_url.netloc, '')
        last_result = False
        result_set = None
        number_of_triples_per_repo = len(reduced_mapping.mapping)
        query = ''
        query_parameters = {}
        github = GithubApi()
        for subject_prefix in reduced_mapping.logical_sources:
            if tpq.subject is None or tpq.subject.startswith(subject_prefix):
                query_url = reduced_mapping.logical_sources[subject_prefix]['query']
        if tpq.subject is None and tpq.obj is None:
            query = "e"
        else:
            if tpq.subject:
                full_name = tpq.subject.rpartition('/')[2]
                query = "%s %s" % (query, GITHUB_QUALIFIERS['$.full_name'] % full_name)
                last_result = True
            if tpq.predicate:
                if tpq.obj:
                    for s, p, o in reduced_mapping.mapping:
                        if '%s' % o in GITHUB_QUALIFIERS:
                            query = "%s %s" % (query, GITHUB_QUALIFIERS['%s' % o] % '%s' % tpq.obj)
                        else:
                            query = "%s %s" % (query, '%s' % tpq.obj)
        query_url = "%s%s" % (query_url, REPO_SEARCH)
        query_parameters['q'] = query
        query_parameters['page'] = tpq.page
        query_parameters['per_page'] = REPO_PER_PAGE
        parameters = "?%s" % urlencode(query_parameters)
        result_set = github.request("%s%s" % (query_url, parameters))
        total_count = result_set['total_count']
        result_set = result_set['items']
        if (tpq.page * REPO_PER_PAGE) >= total_count:
            last_result = True
        total_nb_triples = total_count * number_of_triples_per_repo
        nb_triple_per_page = REPO_PER_PAGE * number_of_triples_per_repo
        self._frament_fill_meta(tpq, fragment, last_result, total_nb_triples, nb_triple_per_page, request, tpf_url, query_url)
        return result_set

    def _frament_fill_meta(self, tpq, fragment, last_result, total_nb_triples, nb_triple_per_page, request, tpf_url, query_url):
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
        PROV = Namespace("http://www.w3.org/ns/prov#")

        fragment.add_meta_quad(meta_graph, FOAF['primaryTopic'], dataset_base, meta_graph)
        fragment.add_meta_quad(data_graph, HYDRA['member'], data_graph, meta_graph)
        fragment.add_meta_quad(data_graph, RDF.type, VOID['Dataset'], meta_graph)
        fragment.add_meta_quad(data_graph, RDF.type, HYDRA['Collection'], meta_graph)
        fragment.add_meta_quad(data_graph, VOID['subset'], dataset_base, meta_graph)
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
        fragment.add_meta_quad(source, DCTERMS['title'], Literal("TPF Github search API v3"), meta_graph)
        fragment.add_meta_quad(source, DCTERMS['description'], Literal("Triples from the github repo api v3 matching the pattern {?s=%s, ?p=%s, ?o=%s}" % (tpq.subject, tpq.predicate, tpq.obj)), meta_graph)
        fragment.add_meta_quad(source, DCTERMS['source'], data_graph, meta_graph)
        fragment.add_meta_quad(source, HYDRA['totalItems'], Literal(total_nb_triples, datatype=XSD.int), meta_graph)
        fragment.add_meta_quad(source, VOID['triples'], Literal(total_nb_triples, datatype=XSD.int), meta_graph)
        fragment.add_meta_quad(source, HYDRA['itemsPerPage'], Literal(nb_triple_per_page, datatype=XSD.int), meta_graph)
        fragment.add_meta_quad(source, HYDRA['first'], self._tpf_url(dataset_base, 1, tpq.subject, tpq.predicate, tpq.obj), meta_graph)

        fragment.add_meta_quad(source, RDF.type, PROV['Entity'], meta_graph)
        fragment.add_meta_quad(source, PROV['wasDerivedFrom'], URIRef(query_url), meta_graph)
        fragment.add_meta_quad(source, PROV['wasGeneratedBy'], URIRef("https://github.com/benjimor/odmtp-tpf"), meta_graph)
        if tpq.page > 1:
            fragment.add_meta_quad(source, HYDRA['previous'], self._tpf_url(dataset_base, tpq.page - 1, tpq.subject, tpq.predicate, tpq.obj), meta_graph)
        if not last_result:
            fragment.add_meta_quad(source, HYDRA['next'], self._tpf_url(dataset_base, tpq.page + 1, tpq.subject, tpq.predicate, tpq.obj), meta_graph)
        fragment.add_prefix('twittertpf', Namespace("%s#" % tpf_url[:-1]))
        fragment.add_prefix('void', VOID)
        fragment.add_prefix('foaf', FOAF)
        fragment.add_prefix('hydra', HYDRA)
        fragment.add_prefix('purl', Namespace('http://purl.org/dc/terms/'))
        fragment.add_prefix('prov', PROV)

    def _tpf_uri(self, tpf_url, tag=None):
        if tag is None:
            return URIRef(tpf_url)
        return URIRef("%s%s" % (tpf_url[:-1], '#%s' % tag))

    def _tpf_url(self, dataset_base, page, subject, predicate, obj):
        subject_parameter = subject if subject else ''
        predicate_parameter = predicate if predicate else ''
        if obj:
            if isinstance(obj, URIRef):
                object_parameter = obj
            else:
                object_parameter = ('"%s"^^%s' % (obj, obj._datatype))
        else:
            object_parameter = ''
        parameters = {'page': page, 'subject': subject_parameter, 'predicate': predicate_parameter, 'object': object_parameter}
        return URIRef("%s?%s" % (dataset_base, urlencode(parameters)))
