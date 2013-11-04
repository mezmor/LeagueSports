from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.template import Context, RequestContext


def index(request):
    return render(request, 'drafter/index.html')

def league_focus(request, league_id):
    return HttpResponse("League screen placeholder for league: %s" % league_id)

#@login_required
#def account_focus(request):
#    return render_to_response('drafter/index.html', 
#                              {'is_auth' : request.user.is_authenticated()},
#                              context_instance=RequestContext(request))