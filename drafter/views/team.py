from django.shortcuts import render, redirect
from drafter.forms import LeagueCreationForm, LeagueEditForm, UserCreationForm
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from drafter.models import League, User, FantasyTeam, Message, ConnectionTicket
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

"""
Team related views
"""
def team_roster(request, league_id=None, user_id=None):
    team = FantasyTeam.objects.get(league_id=league_id, manager=user_id)
    return render(request, 'drafter/leagues/details/team/roster.html', { 'team': team, 'league_id': league_id })
"""
Team schedule
"""
def team_schedule(request, league_id=None, user_id=None):
    team = FantasyTeam.objects.get(league_id=league_id, manager=user_id)
    league = League.objects.get(id=league_id)
    return render(request, 'drafter/leagues/details/team/schedule.html', { 'team': team, 'league': league, 'league_id': league_id })
"""
Team transactions
"""
def team_transactions(request, league_id=None, user_id=None):
    team = FantasyTeam.objects.get(league_id=league_id, manager=user_id)
    league = League.objects.get(id=league_id)
    return render(request, 'drafter/leagues/details/team/transactions.html', { 'team': team, 'league': league, 'league_id': league_id })
"""
Team draft picks
"""
def team_picks(request, league_id=None, user_id=None):
    team = FantasyTeam.objects.get(league_id=league_id, manager=user_id)
    league = League.objects.get(id=league_id)
    return render(request, 'drafter/leagues/details/team/picks.html', { 'team': team, 'league': league, 'league_id': league_id })
"""
Team settings
"""
@login_required
def team_settings(request, league_id=None, user_id=None):
    team = FantasyTeam.objects.get(league_id=league_id, manager=user_id)
    league = League.objects.get(id=league_id)
    return render(request, 'drafter/leagues/details/team/settings.html', { 'team': team, 'league': league, 'league_id': league_id })

"""
Create a FantasyTeam with given league and user
"""
@login_required
def create_team(request, league_id=None, user_id=None):
    # If the request is a POST we hit the DB and do access checks
    if request.method == 'POST':
        league = League.objects.get(id=league_id)
        # Create a team if there is no team associated with the given (league_id, user_id)
        # and the requesting user is either the league's commish or the given user
        if FantasyTeam.objects.filter(manager=user_id, league=league_id).count() == 0 and (request.user.id == int(user_id) or request.user == league.commish):
            FantasyTeam.objects.create(manager=User.objects.get(id=user_id), league=league)
            try:
                join_request = Message.objects.get(target_league=league, sender=user_id)
                return redirect(reverse('drafter.views.delete_request', kwargs={ 'request_id': join_request.id }))
            except Message.DoesNotExist:
                pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

"""
Remove a user from the given league
Currently deletes the FantasyTeam object assocated with the user and league
TODO: Instead of deleting the FantasyTeam, unset the manager and keep the team object so as to assign a new manager
"""
@login_required
def delete_team(request, league_id=None, user_id=None):
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
