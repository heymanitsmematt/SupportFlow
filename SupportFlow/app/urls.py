from django.conf.urls import patterns, url, include
from django.views.generic import DetailView, ListView
from app.models import *
from app import views

urlpatterns = patterns('',
    url(r'^$', views.empmain, name='empmain'),
  
    )


