from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^twitter/', views.twitter_tpf_server, name='twitter_tpf_server'),
    url(r'^github/', views.github_tpf_server, name='github_tpf_server'),
    url(r'^linkedin/authentification/', views.linkedin_authentication_tpf_server, name='linkedin_authentication_tpf_server'),
    url(r'^linkedin/', views.linkedin_tpf_server, name='linkedin_tpf_server')

]
