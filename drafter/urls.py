from django.conf.urls import patterns, url

from drafter import views

urlpatterns = patterns('',
    url(r'^(?P<league_id>\d+)/?$', views.league_focus),
    url(r'^$', views.index),
)