from django.test import TestCase
from django.core.urlresolvers import reverse
from drafter.models import User, League
from drafter.forms import UserCreationForm, LeagueCreationForm

"""
Responses are HttpResponse objects, .status_code, .context, .templates, [<header_name>]
"""
"""
A user may view two types of teams:
    1) A team they are the owner of
    2) A team they are not the owner of
"""
class TeamViewsTestCase(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(username='testUser', password='test1234')
        self.testLeague = League.objects.create(name="testLeague", public=True, size=12, commish_id=self.testUser.id)
        
    """
    Test the team roster view
    Access: 
        - Auth'd user 
        - Guest user
    Visibility:
        Auth'd user:
        Guest user:
    """
    def test_team_roster(self):
        pass
    
    """
    Test the team schedule view
    Access: 
        - Auth'd user 
        - Guest user
    Visibility:
        Auth'd user:
        Guest user:
    """
    def test_team_schedule(self):
        pass
    
    """
    Test the team transactions view
    Access: 
        - Auth'd user 
        - Guest user
    Visibility:
        Auth'd user:
        Guest user:
    """
    def test_team_transactions(self):
        pass
    
    """
    Test the team picks view
    Access: 
        - Auth'd user 
        - Guest user
    Visibility:
        Auth'd user:
        Guest user:
    """
    def test_team_picks(self):
        pass
    
    """
    Test the team settings view
    Access: 
        - Auth'd user 
            - Commish user has access
            - Team owner has access
            - Otherwise redirect
        - Guest user redirects
    Visibility:
        Auth'd user (Commish/Manager):
    """
    def test_team_settings(self):
        pass
    
    """
    Test the team creation view
    Access: 
        - Auth'd user has access
        - Guest user redirects
    Visibility:
        Auth'd user:
        Guest user:
    """
    def test_team_creation(self):
        pass
    
    """
    Test the team deletion view
    Access: 
        - Auth'd user
            - Commish user has access
            - Team owner has access
            - Otherwise redirect
        - Guest user redirects
    Visibility:
        Auth'd user:
        Guest user:
    """
    def test_team_deletion(self):
        pass