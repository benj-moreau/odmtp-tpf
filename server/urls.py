from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^twitter/mapping/extended', views.twitter_extended_mapping, name='twitter_extended_mapping'),
    url(r'^twitter/mapping', views.twitter_mapping, name='twitter_mapping'),
    url(r'^twitter/extended', views.extended_twitter_tpf_server, name='extended_twitter_tpf_server'),
    url(r'^twitter/', views.twitter_tpf_server, name='twitter_tpf_server'),
    url(r'^github/mapping/extended', views.github_extended_mapping, name='github_extended_mapping'),
    url(r'^github/mapping', views.github_mapping, name='github_mapping'),
    url(r'^github/extended', views.extended_github_tpf_server, name='extended_github_tpf_server'),
    url(r'^github/', views.github_tpf_server, name='github_tpf_server'),
    url(r'^linkedin/mapping/extended', views.linkedin_extended_mapping, name='linkedin_extended_mapping'),
    url(r'^linkedin/mapping', views.linkedin_mapping, name='linkedin_mapping'),
    url(r'^linkedin/authentification/', views.linkedin_authentication_tpf_server, name='linkedin_authentication_tpf_server'),
    url(r'^linkedin/extended', views.extended_linkedin_tpf_server, name='extended_linkedin_tpf_server'),
    url(r'^linkedin/', views.linkedin_tpf_server, name='linkedin_tpf_server')

]
