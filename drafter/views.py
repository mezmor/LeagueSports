from django.shortcuts import render
from drafter.forms import LeagueForm
from django.contrib.auth.decorators import login_required
from drafter.models import League


def index(request):
    # if request is POST, register the user
    return render(request, 'drafter/index.html')

def leagues(request):
    leagues = list(League.objects.all())
    return render(request, 'drafter/league/leagues.html', { 'leagues': leagues })

def league(request, id):
    league = League.objects.get(id=id)
    return render(request, 'drafter/league/league.html', { 'league': league })

@login_required
def new_league(request):
    if request.method == 'POST': # If the form was submitted...
        form = LeagueForm(request.POST) # Make a form bound to the POST data
        if form.is_valid():
            new_league = form.save(commit=False)
            new_league.commish = request.user
            new_league.save()
            return leagues(request) 
    else:
        form = LeagueForm() # Unbound form
        
    return render(request, 'drafter/league/new.html', { 'form': form })
