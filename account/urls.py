from django.conf.urls import url, include
from . import views


urlpatterns = [
    # url(r'^$', views.show_profile),
    url(r'^logout/$', views.my_login, name="logout"),
    url(r'^login/$', views.my_login, name="login"),
    url(r'^forgot_password/$', views.forgot_password, name="forgot_password"),

    url(r'^cabinet/$', views.ShowProfileView.as_view(), name="cabinet"),
    url(r'^cabinet/change_password/$', views.change_password, name="change_password"),

    url(r'cabinet/experts/', include([
        url(r'^$', views.ExpertList.as_view(), name='experts'),
        url(r'^new/$', views.CreateExpertView.as_view(), name="invite_expert"),
    ])),

    url(r'cabinet/expert/(?P<pk>\d+)/$', views.ExpertView.as_view(), name='expert'),
    url(r'^cabinet/toggle_activity/(\d+)/$', views.toggle_activity, name="toggle_activity"),
    url(r'^cabinet/reset_password/(\w*@\w*\.\w*)/$', views.reset_password, name="reset_password"),
]
