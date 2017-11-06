from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^twitter/', views.twitter_tpf_server, name='twitter_tpf_server'),
    url(r'^github/', views.github_tpf_server, name='github_tpf_server')
]
