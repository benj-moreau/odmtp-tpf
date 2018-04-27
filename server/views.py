from odmtp.odmtp import Odmtp
from odmtp.modules.trimmer_xr2rml_twitter import TrimmerXr2rmlTwitter
from odmtp.modules.trimmer_xr2rml_github import TrimmerXr2rmlGithub
from odmtp.modules.tp2query_twitter import Tp2QueryTwitter
from odmtp.modules.tp2query_github import Tp2QueryGithub
from odmtp.modules.mapper_twitter_xr2rml import MapperTwitterXr2rml
from odmtp.modules.mapper_github_xr2rml import MapperGithubXr2rml

from tpf.tpq import TriplePatternQuery
from tpf.fragment import Fragment

from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def twitter_tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    fragment = Fragment()
    Odmtp(TrimmerXr2rmlTwitter(), Tp2QueryTwitter(), MapperTwitterXr2rml()).match(tpq, fragment, request)
    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="fragment.trig"'
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def github_tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    fragment = Fragment()
    Odmtp(TrimmerXr2rmlGithub(), Tp2QueryGithub(), MapperGithubXr2rml()).match(tpq, fragment, request)
    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="fragment.trig"'
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def linkedin_tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    fragment = Fragment()
    Odmtp(TrimmerXr2rmlTwitter(), Tp2QueryTwitter(), MapperTwitterXr2rml()).match(tpq, fragment, request)
    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="fragment.trig"'
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def linkedin_authentication_tpf_server(request):
    fragment = Fragment()
    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="linkedin_auth.trig"'
    response['Access-Control-Allow-Origin'] = '*'
    return response
