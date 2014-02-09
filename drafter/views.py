from django.shortcuts import render, redirect
from drafter.forms import LeagueForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from drafter.models import League, User, FantasyTeam
from django.core.urlresolvers import reverse


def index(request):
    return render(request, 'drafter/index.html')

"""
User-related views
"""
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
            return redirect(reverse('drafter.views.user', kwargs={ 'id': new_user.id })) 
    else:
        form = UserCreationForm() # Unbound form
    
    return render(request, 'drafter/user/new.html', { 'form': form })    

"""
View a specific user
"""
def user(request, id=None, username=None): # id=None, nick=None, for nick in url?
    if id:
        user = User.objects.get(id=id)
    else:
        user = User.objects.get(username=username)
    return render(request, 'drafter/user/user.html', { 'viewed_user': user })
"""
View all users
"""
def users(request):
    users = list(User.objects.all())
    return render(request, 'drafter/user/users.html', { 'users': users })



"""
League-related views
"""
"""
Create a new league
"""
@login_required
def new_league(request):
    if request.method == 'POST': # If the form was submitted...
        form = LeagueForm(request.POST) # Make a form bound to the POST data
        if form.is_valid():
            new_league = form.save(commit=False)
            new_league.commish = request.user
            new_league.save()
            new_team = FantasyTeam(manager=request.user, league=new_league)
            new_team.save()
            return redirect(reverse('drafter.views.league', kwargs={ 'id': new_team.id })) 
    else:
        form = LeagueForm() # Unbound form
    return render(request, 'drafter/league/new.html', { 'form': form })

"""
View a specific league
not called atm
"""
def league(request, id):
    league = League.objects.get(id=id)
    if league.public or request.user.may_enter_draft(league):
        if request.user.is_authenticated():
            if request.user.is_commish(league):
                request.user.commish = True
            if request.user.may_enter_draft(league):
                request.user.may_draft = True
        teams = FantasyTeam.objects.filter(league=league)
        return render(request, 'drafter/league/league.html', { 'league': league, 'teams': teams })
    else:
        return leagues(request)
    
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
    return render(request, 'drafter/league/leagues.html', { 'all_leagues': all_leagues, 'my_leagues': my_leagues, 'commish_leagues': commish_leagues })

"""
View a league's draft management page
"""
@login_required
def league_draft(request, id=None):
    league = League.objects.get(id=id)
    if league.public or league in request.user.leagues.all() or league.commish == request.user:
        if league.commish == request.user:
            request.user.is_commish = True
        return render(request, 'drafter/league/details/draft.html', { 'league': league })
    else:
        return leagues(request)
    
"""
View a league's standings
"""
def league_standings(request):
    return render(request, 'drafter/league/details/standings.html')

"""
View a league's rosters
"""
def league_rosters(request):
    return render(request, 'drafter/league/details/rosters.html')
    
"""
View a league's scoring rules
"""
def league_scoring(request):
    return render(request, 'drafter/league/details/scoring.html')
"""
View a league's playoff bracket
"""
def league_playoffs(request):
    return render(request, 'drafter/league/details/playoffs.html')

"""
View a league's schedule
"""
def league_schedule(request):
    return render(request, 'drafter/league/details/schedule.html')