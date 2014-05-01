from django.test import TestCase
from django.core.urlresolvers import reverse
from drafter.models import User, League
from drafter.forms import UserCreationForm, LeagueCreationForm

"""
Responses are HttpResponse objects, .status_code, .context, .templates, [<header_name>]
"""

class MessageViewsTestCase(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(username='testUser', password='test1234')
        self.testLeague = League.objects.create(name="testLeague", public=True, size=12, commish_id=self.testUser.id)
    
    """
    Test the new join requests view
    Access: 
        - Auth'd user
            - Commish user has access
            - Standard user redirects
        - Guest user redirects
    Visibility:
    """
    def test_new_requests(self):
        pass
    
    """
    Test the request creation view
    Access: 
        - Auth'd user has access
        - Guest user redirects
        - Verify that a GET redirects, only POST is accepted
    Visibility:
        Auth'd user:
    """
    def test_request_creation(self):
        pass
    
    """
    Test the request deletion view
    Access: 
        - Auth'd user that is the recipient of the request
        - Guest user directs
    """
    def test_request_deletion(self):
        pass