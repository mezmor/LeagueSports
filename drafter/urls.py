from django.conf.urls import *
from django.contrib.auth.views import AuthenticationForm 
from drafter import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    
    url(r'^register/$', views.new_user),
    url(r'^users/$', views.users),
    url(r'^users/(?P<user_id>\d+)/$', views.user),
    url(r'^users/(?P<username>[\w.@+-]+)/$', views.user),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'drafter/index.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/' }),
    
    url(r'^leagues/$', views.leagues),
    url(r'^leagues/new/$', views.new_league),
    url(r'^leagues/(?P<league_id>\d+)/$', views.league),
    url(r'^leagues/(?P<league_id>\d+)/standings/$', views.league_standings),
    url(r'^leagues/(?P<league_id>\d+)/draft/$', views.league_draft),
    url(r'^leagues/(?P<league_id>\d+)/rosters/$', views.league_rosters),
    url(r'^leagues/(?P<league_id>\d+)/scoring/$', views.league_scoring),
    url(r'^leagues/(?P<league_id>\d+)/playoffs/$', views.league_playoffs),
    url(r'^leagues/(?P<league_id>\d+)/schedule/$', views.league_schedule),
    url(r'^leagues/(?P<league_id>\d+)/settings/$', views.league_settings),  
)