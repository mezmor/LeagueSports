from django.conf.urls import patterns, url

from drafter import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<league_id>\d+)$', views.league_focus, name='league_focus'),
    url(r'^(?P<league_id>\d+)/$', views.league_focus, name='league_focus'),
)