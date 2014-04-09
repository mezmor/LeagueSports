from django.conf.urls import *
from drafter import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    
    # User URLs
    url(r'^register/$', views.new_user),
    url(r'^users/$', views.users),
    url(r'^users/(?P<user_id>\d+)/$', views.user),
    url(r'^users/(?P<username>[\w.@+-]+)/$', views.user),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'drafter/index.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page' : '/' }),
    
    # League URLs
    url(r'^leagues/$', views.leagues),
    url(r'^leagues/new/$', views.new_league),
    url(r'^leagues/(?P<league_id>\d+)/$', views.league),
    url(r'^leagues/(?P<league_id>\d+)/standings/$', views.league_standings),
    url(r'^leagues/(?P<league_id>\d+)/draft/$', views.league_draft),
    url(r'^leagues/(?P<league_id>\d+)/rosters/$', views.league_rosters),
    url(r'^leagues/(?P<league_id>\d+)/scoring/$', views.league_scoring),
    url(r'^leagues/(?P<league_id>\d+)/playoffs/$', views.league_playoffs),
    url(r'^leagues/(?P<league_id>\d+)/schedule/$', views.league_schedule),
    
    # Commish settings URLs
    url(r'^leagues/(?P<league_id>\d+)/settings/$', views.league_settings),
    url(r'^leagues/(?P<league_id>\d+)/settings/requests$', views.new_join_requests),
    url(r'^leagues/(?P<league_id>\d+)/settings/draft$', views.league_draft_settings),
    url(r'^requests/(?P<request_id>\d+)/del$', views.del_request),
    
    # FantasyTeam URLs, user-league management
    url(r'^leagues/(?P<league_id>\d+)/join/$', views.join_league),
    url(r'^leagues/(?P<league_id>\d+)/add/(?P<user_id>\d+)$', views.add_user_to_league),
    url(r'^leagues/(?P<league_id>\d+)/del/(?P<user_id>\d+)$', views.del_user_from_league),
    url(r'^leagues/(?P<league_id>\d+)/(?P<user_id>\d+)/roster$', views.team_roster),
    url(r'^leagues/(?P<league_id>\d+)/(?P<user_id>\d+)/schedule$', views.team_schedule),
    url(r'^leagues/(?P<league_id>\d+)/(?P<user_id>\d+)/transactions$', views.team_transactions),
    url(r'^leagues/(?P<league_id>\d+)/(?P<user_id>\d+)/picks$', views.team_picks),
    url(r'^leagues/(?P<league_id>\d+)/(?P<user_id>\d+)/settings$', views.team_settings),
)