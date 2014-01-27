from django.forms import ModelForm, ValidationError
from drafter.models import League, User
from django.contrib.auth.forms import UserCreationForm


class LeagueForm(ModelForm):
    class Meta:
        model = League
        fields = ('name', 'public', 'size')

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
