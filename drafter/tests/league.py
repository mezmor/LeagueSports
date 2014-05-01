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
    Access: Guest user, Auth'd user
    Visibility:
        Guest user:
            - All leagues
                - No join buttons present
        Auth'd user:
            - New league
            - All leagues
                - Join buttons present
                - New request count present
            - My leagues
            - Commish'd leagues
                - New request count present
    """
    def test_league_list(self):
        response = self.client.get(reverse('drafter.views.users'))
        self.assertEqual(response.status_code, 200, "Status code not OK (200): " + str(response.status_code))
    
    """
    Test league creation view
    Test that a logged in user can create a league
    Access: Auth'd user
        - Guest user redirects to homepage
    Visibility:
        Auth'd user:
            - Can create new league
    League creation form should contain:
        - League name
        - League visibility (public?)
        - League size
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
    Access: Auth'd user, Guest user
    Visibility: 
    This is an access point to the league detail page.
    In the future users may change their default landing page from league standings to rosters or another league detail page.
    
    This page should redirect to standings page
    """
    def test_league_default(self):
        response = self.client.get(reverse('drafter.views.league', kwargs={'league_id': self.testLeague.id }))
        self.assertRedirects(response, reverse('drafter.views.league_standings', kwargs={'league_id': self.testLeague.id }))
    
    """
    Test that the navbars in the league detail page behave appropriatley
    Access: Auth'd user, Guest user
    Visibility:
        Auth'd user:
            - Team nav is enabled
            - If commish: Commish Panel button is present
            - If in the league: Draft button is present
        Guest user:
            - Team nav is disabled
            - No Commish Panel button
            - No Draft button
    """
    def test_league_detail_nav(self):
        pass
    
    """
    Test league standings view
    Access: Auth'd user, Guest user
    Visibility:
        Auth'd user:
            - Delete label-button present on auth'd user's team
        Guest user:
            - No delete label-button
    Verify that the correct standings are displayed
    Verify the draft countdown is present on the left
    Verify breadcrumb
    """    
    def test_league_standings(self):
        pass
    
    """
    Test league rosters view
    Access: Auth'd user, Guest user
    Visibility:
        Auth'd user:
        Guest user:
    """
    def test_league_rosters(self):
        pass
    
    """
    Test league scoring view
    Access: Auth'd user, Guest user
    Visibility:
        Auth'd user:
        Guest user:
    """
    def test_league_scoring(self):
        pass
    
    """
    Test league playoff view
    Access: Auth'd user, Guest user
    Visibility:
        Auth'd user:
        Guest user:
    """
    def test_league_playoffs(self):
        pass
    
    """
    Test league schedule view
    Access: Auth'd user, Guest user
    Visibility:
        Auth'd user:
        Guest user:
    """
    def test_league_schedule(self):
        pass
    
    """
    Test league draft view
    This is the real-time drafting app!
    Consider a different test suite for this
    Access: Auth'd user
        - Guest user redirects
    Visibility:
        Auth'd user:
    """
    def test_league_draft(self):
        pass
    
    """
    Test league settings view
    Access: 
        - Auth'd user:
            - Commish user has access
            - Standard user redirects
        - Guest user redirects
    Visibility:
        Commish user:
    
    Verify LeagueEditForm (see drafter/forms.py) has all fields
    """
    def test_league_settings(self):
        pass
    
    """
    Test draft settings view
    Access: 
        - Auth'd user:
            - Commish user has access
            - Standard user redirects
        - Guest user redirects
    Visibility:
        Commish user:
    
    Verify BaseDraftOrderFormSet (drafter/forms.py) has all fields
    """
    def test_draft_settings(self):
        pass
