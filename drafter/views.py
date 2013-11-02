from django.http import HttpResponse


def index(request):
    return HttpResponse("No template yet :(")

def login(request):
    return HttpResponse("Login screen placeholder")

def league_focus(request, league_id):
    return HttpResponse("League screen placeholder for league: %s" % league_id)