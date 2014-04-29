from django.test import TestCase
from django.core.urlresolvers import reverse
from drafter.models import User, League

"""
Responses are HttpResponse objects, .status_code, .context, .templates, [<header_name>]
"""

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(username='testUser', password='test1234')
        self.testLeague = League.objects.create(name="testLeague", public=True, size=12, commish_id=self.testUser.id)
    
    """
    Test the user list view
    """
    def test_user_list(self):
        pass
    
    """
    Test the user creation view
    """
    def test_user_creation(self):
        pass
    
    """
    Test the user detail view
    """
    def test_user_detail(self):
        pass