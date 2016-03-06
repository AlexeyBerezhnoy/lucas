from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^confirm/(\w*@\w*\.\w*)/([1-9A-Z]{4})/$', views.confirm),
    #url(r'^invite_moderator/$', views.invite_moderator),
]
