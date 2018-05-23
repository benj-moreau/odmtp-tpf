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
# me
from django.shortcuts import redirect

from linkedin import linkedin
from django.http import JsonResponse
from django.conf import settings
# pour recupere la date d'aujourd'hui
from time import gmtime, strftime
from datetime import datetime
# pour recuperer l'adresse IP du client
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
        # ecrire le token dans le fichier
        ip = get_client_ip(request)
        json_data = open('/home/amri-c/Documents/odmtp-tpf/utils/users.json', 'r')
        users = json.load(json_data)
        users[ip] = {}
        users[ip]['token'] = linkedin_token[0]
        today = datetime.datetime.now()
        # transform to a string
        users[ip]['Date'] = today.strftime('%Y-%m-%d %H:%M:%S.%f')
        f = open("/home/amri-c/Documents/odmtp-tpf/utils/users.json", "w")
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
            json_data = open('/home/amri-c/Documents/odmtp-tpf/utils/users.json', 'r')
            users = json.load(json_data)
            response = HttpResponse(users[ip]['token'])
            json_data.close()
    return response


# @require_http_methods(['GET'])
# def linkedin_test_token(request):
#     ACCESS_TOKEN = 'AQXd-_mnHlA8XcHbK-88ssSCcD2vFE_RWM33n7niXh9jSJJRxn2lPsoTdsq9Yas60tWWL5Ila4PA_YhhuTbIO5NNcv1uaR9SnHmM0FHQnlB2VvSChYuNhtdbnhPxbz97v2vvzKCUsaxzMGzXNbp1pWGOvdFhpYABPzAO4c_L3tKxhq7DoWTp8WagWTDXxUV1_22xiHVs3MO6eey3GeSGGhAZpEmuW5oUBZUhjyA4qq-Fx1u_RqgynRjCxX-5oBnUomGAHeB6Vgxj7KfRLLxz6BvObtHsd07LQHHWTnSdj1Tlz1r66szCqzVncYsQT3v3t0VJIB8jzddA9IjCnMvxn2z4cA0tTA'
#     application = linkedin.LinkedInApplication(token=ACCESS_TOKEN)
#     # print(dir(application))
#     app = application.get_profile()
#     # app1 = application.get_companies()
#     response = JsonResponse(app, safe=True)
#     return response


# # il faut que la date dans le fichier soit de cette forme "31/12/2015"
# @require_http_methods(['GET'])
# def linkedin_verification_ip_token_date(request):
#     ip = get_client_ip(request)
#     json_data = open('/home/amri-c/Documents/odmtp-tpf/utils/users.json', 'r')
#     users = json.load(json_data)
#     if ip in users:
#         # sauvgarder le token et date correspondant a IP
#         user = users[ip]
#         today = date = datetime.datetime.now()
#         date_use = datetime.strptime(user[1], "%m/%d/%y")
#         tmp = date_use+datetime.timedelta(days=60)
#         if tmp > today:
#             print "le token est toujours valable"
#         else:
#             del users[ip]
#             f = open("user.json", "w")
#             f.write(json.dumps(users, indent=4))
#             f.close()
#             json_data.close()
#             response = redirect('linkedin/authentification/')
#     else:
#         response = redirect('linkedin/authentification/')
#     # appeller directement la vue qui fera la requette en passant en parametre le token
#     # response = HttpResponse("hi")
#     return response
