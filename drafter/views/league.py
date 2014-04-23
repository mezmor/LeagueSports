from django.shortcuts import render, redirect
from drafter.forms import LeagueCreationForm, LeagueEditForm
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from drafter.models import League, FantasyTeam, ConnectionTicket
from django.core.urlresolvers import reverse

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
    """
    We open a websocket to the real-time drafting app on the draft page
    Get the session of the requester and create a ConnectionTicket
    The websocket server will accept/reject the ConnectionTicket
    """
    league = League.objects.get(id=league_id)
    if league in request.user.leagues.all() or league.commish == request.user:
        # Get Session
        sessionid = request.COOKIES.get('sessionid')
        # Create connection ticket, one per user
        try:
            ticket = ConnectionTicket.objects.get(user=request.user)
            ticket.delete()
        except ConnectionTicket.DoesNotExist:
            ticket = None
        
        ticket = ConnectionTicket.objects.create(user=request.user, user_sessionid=sessionid)
        # Send this back to the user?
        
        return render(request, 'drafter/leagues/details/league/draft.html', { 'league_id': league_id, 'league': league })
    else:
        return redirect(reverse('drafter.views.league', kwargs={ 'league_id': league_id }))
"""
from https://devcenter.heroku.com/article/websocket-security
IN THE VIEW:
When the client-side code decides to open a WebSocket, it contacts the HTTP server to obtain an authorization "ticket".   
The server generates this ticket. It typically contains some sort of user/account ID, the IP of the client requesting the ticket, a timestamp, and any other sort of internal record-keeping you might need.
The server stores this ticket (i.e. in a database or cache), and also returns it to the client.
    We open a websocket when the draft page is opened, thus we can create this ticket in the draft view
    We save the ticket pass the generated ticket to the context and send it to the websocket
IN THE SOCKET:
The client opens the WebSocket connection, and sends along this "ticket" as part of an initial handshake.
The server can then compare this ticket, check source IPs, verify that the ticket hasn't been re-used and hasn't expired, and do any other sort of permission checking. If all goes well, the WebSocket connection is now verified.
"""

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
View a league's draft settings
"""
@login_required
def league_draft_settings(request, league_id=None):
    league = League.objects.get(id=league_id)
    if league.commish == request.user:
        DraftOrderFormSet = modelformset_factory(FantasyTeam, fields=("draft_pick", ), max_num=league.teams.count(), extra=0)
        if request.method == 'POST':
            formset = DraftOrderFormSet(request.POST, queryset=FantasyTeam.objects.filter(league=league))
            if formset.is_valid():
                formset.save()
        else:
            formset = DraftOrderFormSet(queryset=FantasyTeam.objects.filter(league=league))
    return render(request, 'drafter/leagues/details/settings/draft.html', { 'league_id': league_id, 'league': league, 'formset': formset})
