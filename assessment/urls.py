from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^assessment/', views.assessment, name='assessment'),
]
