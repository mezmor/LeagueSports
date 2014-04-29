from django.test import TestCase
from django.core.urlresolvers import reverse
from drafter.models import User, League
from drafter.forms import UserCreationForm, LeagueCreationForm

"""
Responses are HttpResponse objects, .status_code, .context, .templates, [<header_name>]
"""

class TeamViewsTestCase(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(username='testUser', password='test1234')
        self.testLeague = League.objects.create(name="testLeague", public=True, size=12, commish_id=self.testUser.id)
        
    """
    Test the team roster view
    """
    def test_team_roster(self):
        pass
    
    """
    Test the team schedule view
    """
    def test_team_schedule(self):
        pass
    
    """
    Test the team transactions view
    """
    def test_team_transactions(self):
        pass
    
    """
    Test the team picks view
    """
    def test_team_picks(self):
        pass
    
    """
    Test the team settings view
    """
    def test_team_settings(self):
        pass
    
    """
    Test the team creation view
    """
    def test_team_creation(self):
        pass
    
    """
    Test the team deletion view
    """
    def test_team_deletion(self):
        pass