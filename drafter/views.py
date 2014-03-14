from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from drafter.forms import LeagueCreationForm, LeagueEditForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from drafter.models import League, User, FantasyTeam, Message
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'drafter/index.html')

"""
User-related views
"""
"""
View all users
"""
def users(request):
    users = list(User.objects.all())
    return render(request, 'drafter/users/users.html', { 'users': users })
"""
Create a new user
"""
def new_user(request):
    if request.method == 'POST': # If the form was submitted...
        form = UserCreationForm(request.POST) # Make a form bound to the POST data
        if form.is_valid():
            new_user = form.save()
            username = request.POST['username']
            password = request.POST['password1']
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect(reverse('drafter.views.user', kwargs={ 'user_id': new_user.id })) 
    else:
        form = UserCreationForm() # Unbound form
    
    return render(request, 'drafter/users/new.html', { 'form': form })    

"""
View a specific user
"""
def user(request, user_id=None, username=None): # id=None, nick=None, for nick in url?
    if user_id:
        user = User.objects.get(id=user_id)
    else:
        user = User.objects.get(username=username)
    return render(request, 'drafter/users/user.html', { 'viewed_user': user })


"""
League-related views
"""
"""
View all leagues
"""
def leagues(request):
    all_leagues = list(League.objects.all())
    if request.user.is_authenticated():
        my_leagues = list(request.user.leagues.all())
        commish_leagues = list(request.user.managed_leagues.all())
    else:
        my_leagues = None
        commish_leagues = None
    return render(request, 'drafter/leagues/leagues.html', { 'all_leagues': all_leagues, 'my_leagues': my_leagues, 'commish_leagues': commish_leagues })

"""
Create a new league
"""
@login_required
def new_league(request):
    if request.method == 'POST': # If the form was submitted...
        form = LeagueCreationForm(request.POST) # Make a form bound to the POST data
        if form.is_valid():
            new_league = form.save(commit=False)
            new_league.commish = request.user
            new_league.save()
            FantasyTeam.objects.create(manager=request.user, league=new_league)
            return redirect(reverse('drafter.views.league', kwargs={ 'league_id': new_league.id })) # TODO: redirect has implicit reverse
    else:
        form = LeagueCreationForm() # Unbound form
    return render(request, 'drafter/leagues/new.html', { 'form': form })

"""
View a specific league's default tab (for now hardcoded to Standings)
"""
def league(request, league_id=None):
    return redirect(reverse('drafter.views.league_standings', kwargs={ 'league_id': league_id })) 

"""
View a league's standings
"""
def league_standings(request, league_id=None):
    league = League.objects.get(id=league_id)
    teams = [(a+1, b) for (a, b) in enumerate(league.teams.all().order_by('wins'))]
    return render(request, 'drafter/leagues/details/league/standings.html', { 'league_id': league_id, 'league': league, 'teams': teams })

"""
View a league's rosters
"""
def league_rosters(request, league_id=None):
    league = League.objects.get(id=league_id)
    return render(request, 'drafter/leagues/details/league/rosters.html', { 'league_id': league_id, 'league': league })
    
"""
View a league's scoring rules
"""
def league_scoring(request, league_id=None):
    league = League.objects.get(id=league_id)
    return render(request, 'drafter/leagues/details/league/scoring.html', { 'league_id': league_id, 'league': league })
"""
View a league's playoff bracket
"""
def league_playoffs(request, league_id=None):
    league = League.objects.get(id=league_id)
    return render(request, 'drafter/leagues/details/league/playoffs.html', { 'league_id': league_id, 'league': league })

"""
View a league's schedule
"""
def league_schedule(request, league_id=None):
    league = League.objects.get(id=league_id)
    return render(request, 'drafter/leagues/details/league/schedule.html', { 'league_id': league_id, 'league': league })
    
"""
View a league's draft management page
"""
@login_required
def league_draft(request, league_id=None):
    league = League.objects.get(id=league_id)
    if league in request.user.leagues.all() or league.commish == request.user:
        return render(request, 'drafter/leagues/details/league/draft.html', { 'league_id': league_id, 'league': league })
    else:
        return redirect(reverse('drafter.views.league', kwargs={ 'league_id': league_id }))
    
"""
View a league's commish panel
"""
@login_required
def league_settings(request, league_id=None):
    league = League.objects.get(id=league_id)
    if league.commish == request.user:
        if request.method == 'POST':
            form = LeagueEditForm(request.POST, instance=league)
            if form.is_valid():
                form.save()
        else:
            form = LeagueEditForm(instance=league) 
        return render(request, 'drafter/leagues/details/settings/settings.html', { 'league_id': league_id, 'league': league, 'form': form })
    else:
        return redirect(reverse('drafter.views.league', kwargs={ 'league_id': league_id }))
    
"""
Request-related views
"""
"""
View a league's join requests
"""
@login_required
def new_join_requests(request, league_id=None):
    league = League.objects.get(id=league_id)
    # Only a commish may see the new requests
    if league.commish == request.user:
        requests = Message.objects.filter(request=True, target_league=league_id, new=True)
        return render(request, 'drafter/leagues/details/settings/requests.html', { 'league_id': league_id, 'league': league, 'requests': requests })
    else:
        return redirect(reverse('drafter.views.league', kwargs={ 'league_id': league_id }))
    
"""
Join request
"""
@login_required
def join_league(request, league_id=None):
    # If the request was a post, hit the DB and do access checks
    if request.method == 'POST':
        league = League.objects.get(id=league_id)
        # If the league is full we return:
        if league.users.count() >= league.size:
            return redirect(reverse('drafter.views.league', kwargs={ 'league_id': league_id }))
        # If the league is public, let the logged in user join
        if league.public:
            FantasyTeam.objects.create(manager=request.user, league=league)
            return redirect(reverse('drafter.views.league', kwargs={ 'league_id': league_id }))
        else:
            # If the league is private, send a join request
            Message.objects.create(sender=User.objects.get(id=request.user.id), recipient=league.commish, target_league=league, request=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

"""
Delete the given join request
"""
@login_required
def del_request(request, request_id=None):
    join_request = Message.objects.get(id=request_id)
    if request.user == join_request.recipient:
        join_request.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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

