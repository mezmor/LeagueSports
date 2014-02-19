from drafter.models import FantasyTeam, User, Message
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

@register.filter
def request_exists(league, user_id):
    return 0 != Message.objects.filter(sender=User.objects.get(id=user_id), target_league=league).count()

@register.filter
def new_requests(league):
    return Message.objects.filter(request=True, target_league=league, new=True).count()

@register.filter
def accept_action(request):
    pass

@register.filter
def deny_action(request):
    pass