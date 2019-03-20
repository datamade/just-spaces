"""
frontend URL Configuration
"""
from django.conf.urls import url

from frontend import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
