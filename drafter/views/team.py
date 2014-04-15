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
