from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.start),
    url(r'^index/$', views.start),
    url(r'^confirm/(\w*@\w*\.\w*)/([1-9A-Z]{4})/$', views.confirm),
    url(r'^logout/$', views.my_login, name="logout"),
    url(r'^login/$', views.my_login, name="login"),
    url(r'^cabinet/$', views.cabinet, name="cabinet"),
    url(r'^cabinet/experts/$', views.show_experts, name="experts"),
    url(r'^cabinet/expert/(\d+)$', views.show_expert, name="expert"),
    url(r'^cabinet/invite_expert/$', views.invite_expert, name="invite_expert"),
]
