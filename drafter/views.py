from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext



def index(request):
    # if request is POST, register the user
    form = UserCreationForm()
    context = { 'register_form' : form,  }
    return render(request, 'drafter/index.html', context, context_instance=RequestContext(request))

def league_focus(request, league_id):
    return HttpResponse("League screen placeholder for league: %s" % league_id)


def tutorial(request):
    return render(request, 'drafter/tutorial.html')

#@login_required
#def account_focus(request):
#    return render_to_response('drafter/index.html', 
#                              {'is_auth' : request.user.is_authenticated()},
#                              context_instance=RequestContext(request))