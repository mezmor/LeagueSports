from django.shortcuts import render
from drafter.forms import LeagueForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from drafter.models import League, User


def index(request):
    return render(request, 'drafter/index.html')

@login_required
def new_league(request):
    if request.method == 'POST': # If the form was submitted...
        form = LeagueForm(request.POST) # Make a form bound to the POST data
        if form.is_valid():
            new_league = form.save(commit=False)
            new_league.commish = request.user
            new_league.save()
            new_league.users.add(request.user)
            return league(request, new_league.id)
    else:
        form = LeagueForm() # Unbound form
        
    return render(request, 'drafter/league/new.html', { 'form': form })

def league(request, id):
    league = League.objects.get(id=id)
    if league.public or request.user.is_draftable(league):
        if request.user.is_commish(league):
            request.user.commish = True
        if request.user.is_draftable(league):
            request.user.draftable = True
        return render(request, 'drafter/league/league.html', { 'league': league })
    else:
        return leagues(request)

def leagues(request):
    leagues = list(League.objects.all())
    return render(request, 'drafter/league/leagues.html', { 'leagues': leagues })

def draft(request, id=None):
    league = League.objects.get(id=id)
    if league.public or league in request.user.leagues.all() or league.commish == request.user:
        if league.commish == request.user:
            request.user.is_commish = True
        return render(request, 'drafter/league/draft.html', { 'league': league })
    else:
        return leagues(request)
    
def new_user(request):
    if request.method == 'POST': # If the form was submitted...
        form = UserCreationForm(request.POST) # Make a form bound to the POST data
        if form.is_valid():
            new_user = form.save()
            return users(request) 
    else:
        form = UserCreationForm() # Unbound form
    
    return render(request, 'drafter/user/new.html', { 'form': form })    

def user(request, id=None, username=None): # id=None, nick=None, for nick in url?
    if id:
        user = User.objects.get(id=id)
    else:
        user = User.objects.get(username=username)
    
    return render(request, 'drafter/user/user.html', { 'user': user })

def users(request):
    users = list(User.objects.all())
    return render(request, 'drafter/user/users.html', { 'users': users })


