from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^$', views.show_profile),
    url(r'^confirm/(\w*@\w*\.\w*)/([1-9A-Z]{4})/$', views.confirm, name="confirm"),
    url(r'^logout/$', views.my_login, name="logout"),
    url(r'^login/$', views.my_login, name="login"),
    url(r'^cabinet/$', views.ShowProfileView.as_view(), name="cabinet"),
    url(r'^cabinet/change_password/$', views.change_password, name="change_password"),
    url(r'^cabinet/experts/$', views.show_experts, name="experts"),
    url(r'^cabinet/expert/(\d+)$', views.show_expert, name="expert"),
    url(r'^cabinet/invite_expert/$', views.new_expert, name="invite_expert"),
    url(r'^cabinet/edit_expert/(\d+)/$', views.edit_expert, name="edit_expert"),
    url(r'^cabinet/del_expert/(\d+)/$', views.del_expert, name="del_expert"),
    url(r'^cabinet/toggle_activity/(\d+)/$', views.toggle_activity, name="toggle_activity"),
    url(r'^cabinet/reset_password/(\w*@\w*\.\w*)/$', views.reset_password, name="reset_password"),
    url(r'^cabinet/forgot_password/$', views.forgot_password, name="forgot_password"),
]
