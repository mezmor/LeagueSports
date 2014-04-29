from django.test import TestCase
from django.core.urlresolvers import reverse
from drafter.models import User, League
from drafter.forms import UserCreationForm, LeagueCreationForm

"""
Responses are HttpResponse objects, .status_code, .context, .templates, [<header_name>]
"""

class GeneralViewsTestCase(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(username='testUser', password='test1234')
        self.testLeague = League.objects.create(name="testLeague", public=True, size=12, commish_id=self.testUser.id)
        
    """
    Test the index view
    """    
    def test_index(self):
        response = self.client.get(reverse('drafter.views.index'))
        self.assertEqual(response.status_code, 200, "Status code not OK (200): " + str(response.status_code))
        