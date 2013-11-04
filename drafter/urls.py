from django.conf.urls import patterns, url

from drafter import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^(?P<league_id>\d+)/?$', views.league_focus),
    #url(r'^login/$', views.login)
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'drafter/index.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : '../'}),
)