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
        
    