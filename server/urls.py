from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.tpf_server, name='tpf_server'),
]
