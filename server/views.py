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
from utils.rml_closer import OWLLiteCloser, RDFSCloser

from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect

from linkedin import linkedin
from django.conf import settings
from datetime import datetime
from rdflib import Graph
import json
import os


@require_http_methods(['GET', 'HEAD', 'OPTIONS'])
def twitter_tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    fragment = Fragment()
    odmtp = request.session.get('odmtp_twitter')
    if not odmtp:
        odmtp = Odmtp(TrimmerXr2rmlTwitter(), Tp2QueryTwitter(), MapperTwitterXr2rml())
        request.session['odmtp_twitter'] = odmtp
    odmtp.match(tpq, fragment, request)
    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="twitter_tpf_fragment.trig"'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Accept-Datetime,Accept'
    return response


@require_http_methods(['GET', 'HEAD', 'OPTIONS'])
def extended_twitter_tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    fragment = Fragment()
    odmtp = request.session.get('extended_odmtp_twitter')
    if not odmtp:
        odmtp = Odmtp(TrimmerXr2rmlTwitter(True), Tp2QueryTwitter(), MapperTwitterXr2rml())
        request.session['extended_odmtp_twitter'] = odmtp
    odmtp.match(tpq, fragment, request, extended=True)
    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="twitter_tpf_fragment.trig"'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Accept-Datetime,Accept'
    return response


@require_http_methods(['GET'])
def twitter_mapping(request):
    mapping = Graph().parse('./mapping/mapping_tweet.ttl', format='ttl')
    response = HttpResponse(
        mapping.serialize(format='turtle'),
        content_type='text/turtle; charset=utf-8')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def twitter_extended_mapping(request):
    extended_mapping = Graph().parse('./mapping/mapping_tweet.ttl', format='ttl')
    rml_closer = OWLLiteCloser()
    rml_closer.setOnto(Graph().parse('./ontologie/twitter_ontologie.ttl', format='ttl'))
    rml_closer.setRML(extended_mapping)
    rml_closer.enrich()
    extended_mapping = rml_closer.rml
    rml_closer = RDFSCloser()
    rml_closer.setOnto(Graph().parse('./ontologie/twitter_ontologie.ttl', format='ttl'))
    rml_closer.setRML(extended_mapping)
    rml_closer.enrich()
    extended_mapping = rml_closer.rml
    response = HttpResponse(
        extended_mapping.serialize(format='turtle'),
        content_type='text/turtle; charset=utf-8')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET', 'HEAD', 'OPTIONS'])
def github_tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    fragment = Fragment()
    odmtp = request.session.get('odmtp_github')
    if not odmtp:
        odmtp = Odmtp(TrimmerXr2rmlGithub(), Tp2QueryGithub(), MapperGithubXr2rml())
        request.session['odmtp_github'] = odmtp
    odmtp.match(tpq, fragment, request)
    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="github_tpf_fragment.trig"'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Accept-Datetime,Accept'
    return response


@require_http_methods(['GET', 'HEAD', 'OPTIONS'])
def extended_github_tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    fragment = Fragment()
    odmtp = request.session.get('extended_odmtp_github')
    if not odmtp:
        odmtp = Odmtp(TrimmerXr2rmlGithub(True), Tp2QueryGithub(), MapperGithubXr2rml())
        request.session['extended_odmtp_github'] = odmtp
    odmtp.match(tpq, fragment, request, extended=True)
    response = HttpResponse(
        fragment.serialize(),
        content_type='application/trig; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="github_tpf_fragment.trig"'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Accept-Datetime,Accept'
    return response


@require_http_methods(['GET'])
def github_mapping(request):
    mapping = Graph().parse('./mapping/mapping_github.ttl', format='ttl')
    response = HttpResponse(
        mapping.serialize(format='turtle'),
        content_type='text/turtle; charset=utf-8')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def github_extended_mapping(request):
    extended_mapping = Graph().parse('./mapping/mapping_github.ttl', format='ttl')
    rml_closer = OWLLiteCloser()
    rml_closer.setOnto(Graph().parse('./ontologie/github_ontologie.ttl', format='ttl'))
    rml_closer.setRML(extended_mapping)
    rml_closer.enrich()
    extended_mapping = rml_closer.rml
    rml_closer = RDFSCloser()
    rml_closer.setOnto(Graph().parse('./ontologie/github_ontologie.ttl', format='ttl'))
    rml_closer.setRML(extended_mapping)
    rml_closer.enrich()
    extended_mapping = rml_closer.rml
    response = HttpResponse(
        extended_mapping.serialize(format='turtle'),
        content_type='text/turtle; charset=utf-8')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Accept-Datetime,Accept'
    return response


@require_http_methods(['GET', 'HEAD', 'OPTIONS'])
def linkedin_tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    fragment = Fragment()
    try:
        odmtp = request.session.get('odmtp_linkedin')
        if not odmtp:
            odmtp = Odmtp(TrimmerXr2rmllinkedin(), Tp2QueryLinkedin(), MapperlinkedinXr2rml())
            request.session['odmtp_linkedin'] = odmtp
        odmtp.match(tpq, fragment, request)
        response = HttpResponse(
            fragment.serialize(),
            content_type='application/trig; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="linkedin_tpf_fragment.trig"'
    except ValueError:
        response = HttpResponse("You need to be authenticated first. Go to linkedin/authentification/")
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Accept-Datetime,Accept'
    return response


@require_http_methods(['GET', 'HEAD', 'OPTIONS'])
def extended_linkedin_tpf_server(request):
    tpq = TriplePatternQuery(request.GET.get('page', '1'),
                             request.GET.get('subject'),
                             request.GET.get('predicate'),
                             request.GET.get('object'))
    fragment = Fragment()
    try:
        odmtp = request.session.get('extended_odmtp_linkedin')
        if not odmtp:
            odmtp = Odmtp(TrimmerXr2rmllinkedin(True), Tp2QueryLinkedin(), MapperlinkedinXr2rml())
            request.session['extended_odmtp_linkedin'] = odmtp
        odmtp.match(tpq, fragment, request, extended=True)
        response = HttpResponse(
            fragment.serialize(),
            content_type='application/trig; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="linkedin_tpf_fragment.trig"'
    except ValueError:
        response = HttpResponse("You need to be authenticated first. Go to linkedin/authentification/")
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Accept-Datetime,Accept'
    return response


@require_http_methods(['GET'])
def linkedin_mapping(request):
    mapping = Graph().parse('./mapping/mapping_linkedin.ttl', format='ttl')
    response = HttpResponse(
        mapping.serialize(format='turtle'),
        content_type='text/turtle; charset=utf-8')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def linkedin_extended_mapping(request):
    extended_mapping = Graph().parse('./mapping/mapping_linkedin.ttl', format='ttl')
    rml_closer = OWLLiteCloser()
    rml_closer.setOnto(Graph().parse('./ontologie/linkedin_ontologie.ttl', format='ttl'))
    rml_closer.setRML(extended_mapping)
    rml_closer.enrich()
    extended_mapping = rml_closer.rml
    rml_closer = RDFSCloser()
    rml_closer.setOnto(Graph().parse('./ontologie/linkedin_ontologie.ttl', format='ttl'))
    rml_closer.setRML(extended_mapping)
    rml_closer.enrich()
    extended_mapping = rml_closer.rml
    response = HttpResponse(
        extended_mapping.serialize(format='turtle'),
        content_type='text/turtle; charset=utf-8')
    response['Access-Control-Allow-Origin'] = '*'
    return response


@require_http_methods(['GET'])
def linkedin_authentication_tpf_server(request):
    authentication = linkedin.LinkedInAuthentication(settings.CLIENT_ID_LINKEDIN, settings.CLIENT_SECRET_LINKEDIN, "http://{}/linkedin/authentification/".format(request.get_host()), ['r_emailaddress', 'r_basicprofile', 'w_share', 'rw_company_admin'])
    authorization_code = request.GET.get('code', None)
    if authorization_code:
        authentication.authorization_code = authorization_code
        linkedin_token = authentication.get_access_token()
        ip = get_client_ip(request)
        json_data = open(os.path.abspath('utils/users.json'), 'r')
        users = json.load(json_data)
        users[ip] = {}
        users[ip]['token'] = linkedin_token[0]
        today = datetime.now()
        users[ip]['Date'] = today.strftime('%Y-%m-%d %H:%M:%S.%f')
        f = open(os.path.abspath('utils/users.json'), "w")
        f.write(json.dumps(users, indent=4))
        f.close()
        json_data.close()
        response = redirect('http://client.linkeddatafragments.org/#datasources=http%3A%2F%2Fodmtp.priloo.univ-nantes.fr%2Flinkedin%2F&query=SELECT%20%3Fs%20%3Fp%20%3Fo%0AWHERE%20%7B%0A%20%3Fs%20%3Fp%20%3Fo%0A%7D')
    else:
        if not linkedin_verification_ip_token_date(request):
            linkedin.LinkedInApplication(authentication)
            response = redirect(authentication.authorization_url)
        else:
            ip = get_client_ip(request)
            json_data = open(os.path.abspath('utils/users.json'), 'r')
            users = json.load(json_data)
            response = redirect('http://client.linkeddatafragments.org/#datasources=http%3A%2F%2Fodmtp.priloo.univ-nantes.fr%2Flinkedin%2F&query=SELECT%20%3Fs%20%3Fp%20%3Fo%0AWHERE%20%7B%0A%20%3Fs%20%3Fp%20%3Fo%0A%7D')
            json_data.close()
    response['Access-Control-Allow-Origin'] = '*'
    return response
