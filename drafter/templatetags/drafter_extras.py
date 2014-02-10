from drafter.models import FantasyTeam
from django import template

register = template.Library()

@register.filter
def has_team(user, league):
    return user.is_authenticated() and FantasyTeam.objects.filter(manager=user, league=league).count() > 0

@register.filter
def may_enter_draft(user, league):
    return user.is_authenticated() and user.may_enter_draft(league)

@register.filter
def is_commish(user, league):
    return league.commish == user
