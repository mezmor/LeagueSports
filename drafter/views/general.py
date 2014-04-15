from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from drafter.models import League, User, FantasyTeam, Message
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

"""
Frontpage
"""
def index(request):
    return render(request, 'drafter/index.html')

"""
League interaction views
"""
"""
Create a FantasyTeam with given league and user
"""
@login_required
def add_user_to_league(request, league_id=None, user_id=None):
    # If the request is a POST we hit the DB and do access checks
    if request.method == 'POST':
        league = League.objects.get(id=league_id)
        # If there is already a team associated with this user
        # or if the requester is not the league commish, they can not add a user to the league, so redirect
        if FantasyTeam.objects.filter(manager=user_id, league=league_id).count() > 0 or not request.user == league.commish:
            return redirect(reverse('drafter.views.league', kwargs={ 'league_id': league_id }))
        
        FantasyTeam.objects.create(manager=User.objects.get(id=user_id), league=league)
        join_request = Message.objects.get(target_league=league, sender=user_id)
        return redirect(reverse('drafter.views.del_request', kwargs={ 'request_id': join_request.id }))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

"""
Remove a user from the given league
Currently deletes the FantasyTeam object assocated with the user and league
TODO: Instead of deleting the FantasyTeam, unset the manager and keep the team object so as to assign a new manager
"""
@login_required
def del_user_from_league(request, league_id=None, user_id=None):
    if request.method == 'POST':
        league = League.objects.get(id=league_id)
        # Try to get a team associated with the user and league
        try:
            team = FantasyTeam.objects.get(league=league, manager=user_id)
        except FantasyTeam.DoesNotExist:
            team = None
        # Delete the FantasyTeam object if the requester is the user or the league commish and the team exists
        if request.user.id == int(user_id) or request.user == league.commish and team is not None:
            team.delete()
    return redirect(reverse('drafter.views.league', kwargs={ 'league_id': league_id }))
