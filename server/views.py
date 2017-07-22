from odmtrip.odmtrip import Odmtrip
from odmtrip.modules.trimmer_xr2rml import TrimmerXr2rml
from odmtrip.modules.tp2query_twitter import Tp2QueryTwitter
from tpf.tpq import TriplePatternQuery
from tpf.fragment import Fragment

from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    fragment = Fragment()
    reduced_mapping = TrimmerXr2rml().get_reduced_mapping(tpq)
    result_set = Tp2QueryTwitter().request(tpq, reduced_mapping, fragment)
    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="fragment.trig"'
    return response
