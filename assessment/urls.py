from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^qualities/', include([
        url(r'^$', views.QualityList.as_view(), name="qualities"),
        url(r'^create/$', views.CreateQuality.as_view(), name="new_quality"),
        url(r'^rate/$', views.RateQualities.as_view(), name="edit_assessments"),
    ])),
    url(r'^quality/(?P<pk>\d+)/', include([
        url(r'^edit/$', views.EditQuality.as_view(), name="edit_quality"),
        url(r'^delete/$', views.DeleteQuality.as_view(), name="del_quality"),
    ])),
]
