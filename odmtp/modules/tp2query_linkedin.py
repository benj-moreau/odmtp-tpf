from rdflib import URIRef, Literal, Namespace, BNode, RDF, XSD
from urllib import urlencode
from urlparse import urlparse


from odmtp.modules.tp2query import Tp2Query
from linkedin import linkedin


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
# a modifier pour linkedin
TWEETS_PER_PAGE = 5

TPF_URL = '%s://%s/twitter/'

# twitter search API returns top 15000 tweets matching query
# So i set up a limit to count maximum number of result (TWEETS_PER_PAGE * LAST_PAGE)
LAST_PAGE = 5


class Tp2QueryTwitter(Tp2Query):

    def request(self, tpq, reduced_mapping, fragment, request):
        # comment recupérer le token , appeller l'aithentification ? comment recupérer l'adresse IP pour recoupérer les corrects données sur le fichier
        # appler la vus de l'authentification ici ?
        # ou recuperer l'adresse ip et le token et aller chercher ca dans le fichier
        # si le recuperer dans le fichier

        # le retour est une requete http comment prendre que le token si je fait deux renvoie sur la vue est-ce-que cela fonctionnerai
        # ACCESS_TOKEN = redirect('linkedin/authentification/')
        # application = linkedin.LinkedInApplication(token=ACCESS_TOKEN)
        # result_set = application.get_profile()
        # # response = JsonResponse(app, safe=True)
        result_set = 0
        return result_set

    def _frament_fill_meta(self, tpq, fragment, last_result, total_nb_triples, nb_triple_per_page, request, tpf_url):
        # meta_graph = uri de refrence metadata#
        meta_graph = self._tpf_uri(tpf_url, 'metadata')
        # j'insere les metadonnees en tant que graphe(triplet) dans mon fragment
        fragment.add_graph(meta_graph)
        # meme chose que la premire ligne
        dataset_base = self._tpf_uri(tpf_url)
        # creer une uri avec ce qui est passse en parametre elle de quel forme la request c'est untripple pattern fragment
        source = URIRef(request.build_absolute_uri())
        # ecrit en chaine de caractere avec le dataset_base donc l'uri suivie du spo
        dataset_template = Literal('%s%s' % (dataset_base, '{?subject,predicate,object}'))
        # uri avec data_set à la suite
        data_graph = self._tpf_uri(tpf_url, 'dataset')
        # noms donné a soit un sujet ou un objet
        tp_node = BNode('triplePattern')
        subject_node = BNode('subject')
        predicate_node = BNode('predicate')
        object_node = BNode('object')
        # je dois ajouter quoi comme liens ?
        # uri dbpedia ?
        DBPEDIA = Namespace("http://dbpedia.org/ontology#")
        SHEMA = Namespace("http://schema.org")

        HYDRA = Namespace("http://www.w3.org/ns/hydra/core#")
        VOID = Namespace("http://rdfs.org/ns/void#")
        FOAF = Namespace("http://xmlns.com/foaf/0.1/")
        DCTERMS = Namespace("http://purl.org/dc/terms/")

        fragment.add_meta_quad(meta_graph, FOAF['primaryTopic'], dataset_base, meta_graph)
        # fragment.add_meta_quad(data_graph, HYDRA['member'], data_graph, meta_graph)
        fragment.add_meta_quad(data_graph, RDF.type, VOID['Dataset'], meta_graph)
        fragment.add_meta_quad(data_graph, RDF.type, HYDRA['Collection'], meta_graph)
        fragment.add_meta_quad(data_graph, VOID['subset'], source, meta_graph)
        # # je n'ai pas besoin d'un endpoint pour linked in
        # fragment.add_meta_quad(data_graph, VOID['uriLookupEndpoint'], dataset_template, meta_graph)
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
        fragment.add_meta_quad(source, DCTERMS['title'], Literal("TPF Linkedin API"), meta_graph)
        fragment.add_meta_quad(source, DCTERMS['description'], Literal("Triple Pattern from the linkedin api matching the pattern {?s=%s, ?p=%s, ?o=%s}" % (tpq.subject, tpq.predicate, tpq.obj)), meta_graph)
        fragment.add_meta_quad(source, DCTERMS['source'], data_graph, meta_graph)

        # ceux dont il m'a parlé mais a quel moment il entre les valeurs ?
        fragment.add_meta_quad(source, HYDRA['totalItems'], Literal(total_nb_triples, datatype=XSD.int), meta_graph)
        fragment.add_meta_quad(source, VOID['triples'], Literal(total_nb_triples, datatype=XSD.int), meta_graph)
        fragment.add_meta_quad(source, HYDRA['itemsPerPage'], Literal(nb_triple_per_page, datatype=XSD.int), meta_graph)
        fragment.add_meta_quad(source, HYDRA['first'], self._tpf_url(dataset_base, 1, tpq.subject, tpq.predicate, tpq.obj), meta_graph)
        if tpq.page > 1:
            fragment.add_meta_quad(source, HYDRA['previous'], self._tpf_url(dataset_base, tpq.page - 1, tpq.subject, tpq.predicate, tpq.obj), meta_graph)
        if not last_result:
            # c'est toujour le dernier resultat estceque je le laisse ou je l'enlève
            # sur linked in toujours une suele page donc previous et next ne s'affiche pas
            fragment.add_meta_quad(source, HYDRA['next'], self._tpf_url(dataset_base, tpq.page + 1, tpq.subject, tpq.predicate, tpq.obj), meta_graph)
        fragment.add_prefix('linkedintpf', Namespace("%s#" % tpf_url[:-1]))
        fragment.add_prefix('void', VOID)
        fragment.add_prefix('foaf', FOAF)
        fragment.add_prefix('hydra', HYDRA)
        fragment.add_prefix('purl', Namespace('http://purl.org/dc/terms/'))
        # ajouter pour dbpedia shema pas sure dutout
        fragment.add_prefix('dbpedia', DBPEDIA)
        fragment.add_prefix('dbpedia', SHEMA)

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
