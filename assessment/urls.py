from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^qualities/$', views.show_qualities, name="qualities"),
    url(r'^quality/$', views.new_quality, name="new_quality"),
    url(r'^quality/(\d+)/$', views.edit_quality, name="edit_quality"),
    url(r'^del_quality/(\d+)/$', views.del_quality, name="del_quality"),
    url(r'^assessments/$', views.show_assessments, name="assessments"),
    url(r'^assessment/(\d+)/$', views.new_assessment, name="new_assessment"),
]
