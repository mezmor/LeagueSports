from django.forms import ModelForm, ValidationError
from django.forms.models import BaseModelFormSet
from drafter.models import League, User, FantasyTeam
from django.contrib.auth.forms import UserCreationForm


class LeagueCreationForm(ModelForm):
    class Meta:
        model = League
        fields = ('name', 'public', 'size')
        
class LeagueEditForm(ModelForm):
    class Meta:
        model = League
        fields = ('name', 'public', 'size', 'draft_start', 'season', 'region', 
                  'transactions_per_time_period', 'transaction_time_period', 'team_size', 
                  'commish', 'top_score', 'jungle_score', 'mid_score', 'ad_score', 'support_score', 
                  'per_game_losing_mod', 'per_game_godly_mod', 'season_length')
        
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", )
        
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(self.error_messages['duplicate_username']) 

class BaseDraftOrderFormSet(BaseModelFormSet):
    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        picks = []
        for form in self.forms:
            pick = form.cleaned_data["draft_pick"]
            if pick in picks:
                raise ValidationError("Draft picks must be distinct")
            elif pick > form.instance.league.size:
                raise ValidationError("Draft pick can not exceed number of teams in the league")
            picks.append(pick)
        
        