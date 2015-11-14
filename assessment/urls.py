from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^experts/$', views.get_experts),
    url(r'^quality/$', views.get_quality),
    url(r'^assessment/$', views.get_assessments),
]
