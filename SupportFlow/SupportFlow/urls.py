from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import views
from app.models import *


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('app.urls', namespace="app")),
    url(r'^flow/(?P<parent_id>[0-9])/$', views.flower, name = 'flow'),
    url(r'^nsjiraapi/MOSO-(?P<jiraIssueKey>[0-9]{4})/$', views.nsjiraapi, name='nsjiraapi'),
    url(r'^nodeshift/$', views.node, '', name='nodeshift'), 
    url(r'^node_edit/$', views.node_edit, name='node_edit'), 
    url(r'^pdfsearch/$', views.pdfsearch, name='pdfsearch'),
    url(r'^ticket/$', views.ticket, name='ticket'),
    url(r'^updateTrackedTickets/$', views.updateTrackedTicketStatus, name='updateTrackedTicketStatus'),
    url(r'^saveNetsuiteTicket/$', views.saveNetsuiteTicket, name='saveNetsuiteTicket'),
    url(r'^updateNetsuiteTickets/$', views.updateNetsuiteTickets, name='updateNetsuiteTickets'),
    url(r'^refreshJiraFromNs/$', views.refreshJiraFromNs, name = 'refreshJiraFromNS'), 
    url(r'^admin/', include(admin.site.urls)),
    )
