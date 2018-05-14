from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^twitter/', views.twitter_tpf_server, name='twitter_tpf_server'),
    url(r'^github/', views.github_tpf_server, name='github_tpf_server'),
    url(r'^linkedin/authentication/', views.linkedin_authentication_tpf_server, name='linkedin_authentication_tpf_server'),
    # url(r'^linkedin/linkedin_test_token/', views.linkedin_test_token, name='linkedin_test_token'),
    url(r'^linkedin/test_token_date/', views.linkedin_verification_ip_token_date, name='linkedin_verification_ip_token_date'),
    url(r'^linkedin/', views.linkedin_tpf_server, name='linkedin_tpf_server')

]
