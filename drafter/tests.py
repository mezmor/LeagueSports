from django.test import TestCase
from django.core.urlresolvers import reverse
from drafter.models import User, League
from drafter.forms import UserCreationForm, LeagueForm

"""
Responses are HttpResponse objects, .status_code, .context, .templates, [<header_name>]
"""

class DrafterViewsTestCase(TestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(username='testUser', password='test1234')
        self.testLeague = League.objects.create(name="testLeague", public=True, size=12, commish_id=self.testUser.id)
    """
    Test the main site
    """    
    def test_index(self):
        response = self.client.get(reverse('drafter.views.index'))
        self.assertEqual(response.status_code, 200, "Status code not OK (200): " + str(response.status_code))
        
    """
    Test user creation view
    Test that a form is provided by the response
    Test that a UserCreationForm can be correctly instantiated
    Test that posting a form will create the user and redirect us to their detail view
    """
    def test_user_creation(self):
        test_user_data = {'username': "test", 'password1': "test1234", 'password2': "test1234"}
        # Test form presence
        response = self.client.get(reverse('drafter.views.new_user'))
        self.assertTrue('form' in response.context)
        # Test form fields
        form = UserCreationForm(data = test_user_data)
        self.assertTrue(form.is_valid())
        # Test user creation via form post and redirect
        form.cleaned_data['csrfmiddlewaretoken'] = [self.client.cookies['csrftoken'].value]
        response = self.client.post(reverse('drafter.views.new_user'), form.cleaned_data)
        test_user_obj = User.objects.get(username=test_user_data['username']) 
        self.assertRedirects(response, reverse('drafter.views.user', kwargs={'id': test_user_obj.id }))
        
    """
    Test user detail view
    """
    def test_user_detail(self):
        response = self.client.get(reverse('drafter.views.user', kwargs={'id': self.testUser.id }))
        self.assertEqual(response.status_code, 200, "Status code not OK (200): " + str(response.status_code))
    """
    Test user list view
    """
    def test_user_list(self):
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
        form = LeagueForm(data = test_league_data)
        self.assertTrue(form.is_valid())
        # Test league creation via form post and redirect
        form.cleaned_data['csrfmiddlewaretoken'] = [self.client.cookies['csrftoken'].value]
        response = self.client.post(reverse('drafter.views.new_league'), form.cleaned_data)
        test_league_obj = League.objects.get(name=test_league_data['name'])
        self.assertRedirects(response, reverse('drafter.views.league', kwargs={'id': test_league_obj.id-1 }))
        
    """
    Test league detail view
    """
    def test_league_detail(self):
        response = self.client.get(reverse('drafter.views.league', kwargs={'id': self.testLeague.id }))
        self.assertEqual(response.status_code, 200, "Status code not OK (200)")
    """
    Test league list view
    """
    def test_league_list(self):
        response = self.client.get(reverse('drafter.views.users'))
        self.assertEqual(response.status_code, 200, "Status code not OK (200): " + str(response.status_code))
    """
    Test draft detail view
    """
    def test_draft_detail(self):
        pass

