from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404


def index(request):
    return render(request, 'drafter/index.html')

def login(request):
    return HttpResponse("Login screen placeholder")

def league_focus(request, league_id):
    return HttpResponse("League screen placeholder for league: %s" % league_id)