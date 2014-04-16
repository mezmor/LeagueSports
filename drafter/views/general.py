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

