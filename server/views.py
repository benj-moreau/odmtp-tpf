from odmtp.odmtp import Odmtp
from odmtp.modules.trimmer_xr2rml_twitter import TrimmerXr2rmlTwitter
from odmtp.modules.trimmer_xr2rml_github import TrimmerXr2rmlGithub
from odmtp.modules.trimmer_xr2rml_linkedin import TrimmerXr2rmllinkedin

from odmtp.modules.tp2query_twitter import Tp2QueryTwitter
from odmtp.modules.tp2query_github import Tp2QueryGithub
from odmtp.modules.tp2query_linkedin import Tp2QueryLinkedin

from odmtp.modules.mapper_twitter_xr2rml import MapperTwitterXr2rml
from odmtp.modules.mapper_github_xr2rml import MapperGithubXr2rml
from odmtp.modules.mapper_linkedin_xr2rml import MapperlinkedinXr2rml

from tpf.tpq import TriplePatternQuery
from tpf.fragment import Fragment

from utils.management_token import get_client_ip, linkedin_verification_ip_token_date

from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect

from linkedin import linkedin
from django.http import JsonResponse
from django.conf import settings
from time import gmtime, strftime
from datetime import datetime
import ipware
import json
import datetime
import os


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
    Odmtp(TrimmerXr2rmllinkedin(), Tp2QueryLinkedin(), MapperlinkedinXr2rml()).match(tpq, fragment, request)
    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="fragment.trig"'
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def linkedin_authentication_tpf_server(request):
    authentication = linkedin.LinkedInAuthentication(settings.CLIENT_ID_LINKEDIN, settings.CLIENT_SECRET_LINKEDIN, "http://127.0.0.1:8000/linkedin/authentification/", ['r_emailaddress', 'r_basicprofile', 'w_share', 'rw_company_admin'])
    authorization_code = request.GET.get('code', None)
    if authorization_code:
        authentication.authorization_code = authorization_code
        linkedin_token = authentication.get_access_token()
        ip = get_client_ip(request)
        json_data = open(os.path.abspath('utils/users.json'), 'r')
        users = json.load(json_data)
        users[ip] = {}
        users[ip]['token'] = linkedin_token[0]
        today = datetime.datetime.now()
        users[ip]['Date'] = today.strftime('%Y-%m-%d %H:%M:%S.%f')
        f = open(os.path.abspath('utils/users.json'), "w")
        f.write(json.dumps(users, indent=4))
        f.close()
        json_data.close()
        response = HttpResponse(linkedin_token[0])
        response['Access-Control-Allow-Origin'] = '*'
    else:
        if not linkedin_verification_ip_token_date(request):
            linkedin.LinkedInApplication(authentication)
            response = redirect(authentication.authorization_url)
        else:
            ip = get_client_ip(request)
            json_data = open(os.path.abspath('utils/users.json'), 'r')
            users = json.load(json_data)
            response = HttpResponse(users[ip]['token'])
            json_data.close()
    return response
