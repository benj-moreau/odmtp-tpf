from odmtrip.odmtrip import Odmtrip
from odmtrip.modules.trimmer_xr2rml import TrimmerXr2rml
from tpf.tpq import TriplePatternQuery
from tpf.fragment import Fragment
from utils.twitter_api import TwitterApi

from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    print tpq.predicate
    fragment = Fragment()
    reduced_mapping = TrimmerXr2rml().get_reduced_mapping(tpq)
    # twitter = TwitterApi()
    # print twitter.request("https://api.twitter.com/1.1/search/tweets.json?q=%23iswc2017")

    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="fragment.trig"'
    return response
