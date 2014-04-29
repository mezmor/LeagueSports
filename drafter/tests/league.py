from django.test import TestCase
from django.core.urlresolvers import reverse
from drafter.models import User, League
from drafter.forms import LeagueCreationForm

"""
Responses are HttpResponse objects, .status_code, .context, .templates, [<header_name>]
"""

class LeagueViewsTestCase(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(username='testUser', password='test1234')
        self.testLeague = League.objects.create(name="testLeague", public=True, size=12, commish_id=self.testUser.id)
    
    """
    Test league list view
    """
    def test_league_list(self):
        response = self.client.get(reverse('drafter.views.users'))
        self.assertEqual(response.status_code, 200, "Status code not OK (200): " + str(response.status_code))
    
    """
    Test league creation view
    Test that a guest gets redirects to homepage 
    Test that a logged in user can create a league
    """
    def test_league_creation(self):
        test_league_data = {'name': 'test league', 'public': 'true', 'size': '12'}
        # Test redirect without log-in
        response = self.client.get(reverse('drafter.views.new_league'))
        # Target url = www.site.com/?next=/leagues/new/, determined by reverse look-up
        self.assertRedirects(response, reverse('drafter.views.index')+'?next='+reverse('drafter.views.new_league'));
        # Test login
        self.assertTrue(self.client.login(username='testUser', password='test1234'))
        # Test form presence
        response = self.client.get(reverse('drafter.views.new_league'))
        self.assertTrue('form' in response.context)
        # TEst form fields
        form = LeagueCreationForm(data = test_league_data)
        self.assertTrue(form.is_valid())
        # Test league creation via form post and redirect
        form.cleaned_data['csrfmiddlewaretoken'] = [self.client.cookies['csrftoken'].value]
        response = self.client.post(reverse('drafter.views.new_league'), form.cleaned_data)
        test_league_obj = League.objects.get(name=test_league_data['name'])
        self.assertRedirects(response, reverse('drafter.views.league', kwargs={'league_id': test_league_obj.id-1 }), target_status_code=302)
        
    """
    Test default league view
    """
    def test_league_default(self):
        response = self.client.get(reverse('drafter.views.league', kwargs={'league_id': self.testLeague.id }))
        self.assertRedirects(response, reverse('drafter.views.league_standings', kwargs={'league_id': self.testLeague.id }))
        
    """
    Test league standings view
    """    
    def test_league_standings(self):
        pass
    
    """
    Test league rosters view
    """
    def test_league_rosters(self):
        pass
    
    """
    Test league scoring view
    """
    def test_league_scoring(self):
        pass
    
    """
    Test league playoff view
    """
    def test_league_playoffs(self):
        pass
    
    """
    Test league schedule view
    """
    def test_league_schedule(self):
        pass
    
    """
    Test league draft view
    This is the real-time drafting app!
    Consider a different test suite for this
    """
    def test_league_draft(self):
        pass
    
    """
    Test league settings view
    """
    def test_league_settings(self):
        pass
    
    """
    Test draft settings view
    """
    def test_draft_settings(self):
        pass
