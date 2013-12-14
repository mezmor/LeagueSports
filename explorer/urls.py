from django.conf.urls import *

from explorer import views

urlpatterns = patterns('',
    url(r'^$', views.explorer),
    url(r'^players/$', views.get_player_names),
)