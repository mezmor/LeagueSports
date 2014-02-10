from drafter.models import FantasyTeam
from django import template

register = template.Library()

@register.filter
def has_team(user, league):
    return FantasyTeam.objects.filter(manager=user, league=league).count() > 0