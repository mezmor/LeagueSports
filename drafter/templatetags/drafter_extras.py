from drafter.models import FantasyTeam, User, Message, League
from django import template
from drafter.forms import RequestCreationForm

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
def get_form(league, user_id):
    form = RequestCreationForm(initial = {'sender': User.objects.get(id=user_id), 'recipient': league.commish, 'target_league': league })
    return form.as_p()

@register.filter
def request_exists(league, user_id):
    return 0 != Message.objects.filter(sender=User.objects.get(id=user_id), target_league=league).count()