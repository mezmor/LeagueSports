from django.forms import ModelForm
from drafter.models import League

class LeagueForm(ModelForm):
    class Meta:
        model = League
        fields = ('name', 'public', 'size')