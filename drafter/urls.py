from django.conf.urls import *

from drafter import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^leagues/$', views.leagues),
    url(r'^league/new/$', views.new_league),
    url(r'^league/(?P<id>\d+)/$', views.league),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'drafter/index.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/' }),
)