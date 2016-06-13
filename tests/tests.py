from django.test import TestCase, override_settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.conf.urls import url, include
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes

from .models import Author, Play, Poem, Kingdom, King, Soldier

User = get_user_model()


# Demo Urls for 
urlpatterns = [
    url('^admin/', include(admin.site.urls)),
]


# Tests 
@override_settings(ROOT_URLCONF=__name__)
class TestMergedInlines(TestCase):
    def setUp(self):
        superuser = User.objects.create_superuser(
            username='super', 
            password='secret', 
            email='super@example.com'
        )

        # Basic Test data
        author = Author.objects.create(name="William Shakespeare")

        play1 = Play.objects.create(
            title='Romeo and Juliet', genre='Tragedy',
            year=1597, author=author, id=1)
        play2 = Play.objects.create(
            title="A Midsummer Night's Dream", genre='Comedy',
            year=1600, author=author, id=3)
        play3 = Play.objects.create(
            title='Julius Caesar', genre='Tragedy',
            year=1623, author=author, id=5)
        

        poem1 = Poem.objects.create(
            title="Shall I compare thee to a summer's day?",
            style="Sonnet", author=author, id=2)
        poem2 = Poem.objects.create(
            title="As a decrepit father takes delight",
            style="Sonnet", author=author, id=4)

        # Custom order field 
        westeros = Kingdom.objects.create(name="Westeros")

        king1 = King.objects.create(
            kingdom=westeros, name="Tommen Baratheon", alive=True, id=1)
        king2 = King.objects.create(
            kingdom=westeros, name="Joffrey Baratheon", alive=False, id=2)
        king3 = King.objects.create(
            kingdom=westeros, name="Rob Stark", alive=False, id=3)

        soldier1 = Soldier.objects.create(
            kingdom=westeros, name="The Hound", house="Brotherhood Without Banners", id=1)
        soldier1 = Soldier.objects.create(
            kingdom=westeros, name="Bronn", house="Lannister?", id=2)

        self.client.login(username='super', password='secret')

    def assertStringOrder(self, response, check_list):
        """
        Check that a list of strings is properly ordered in the content
        """
        index_order = [response.content.index(force_bytes(x)) for x in check_list]

        self.assertEqual(index_order, sorted(index_order))

    def test_basic_merged_view(self):
        """
        With no special settings, the MergedInlineAdmin should order the 
        merged inlines by ID
        """

        response = self.client.get(reverse('admin:tests_author_change', args=(1,)))

        self.assertEqual(response.status_code, 200)
        self.assertStringOrder(response, [
            'Romeo and Juliet',
            'Shall I compare thee to a summer',
            'A Midsummer Night',
            'As a decrepit father takes delight',
            'Julius Caesar',
        ])

    def test_merged_by_custom_field_view(self):
        """
        Specifying a particular merging field
        """

        response = self.client.get(reverse('admin:tests_kingdom_change', args=(1,)))

        self.assertEqual(response.status_code, 200)
        self.assertStringOrder(response, [
            'Bronn',
            'Joffrey Baratheon',
            'Rob Stark',
            'The Hound',
            'Tommen Baratheon'
        ])
        
    def test_custom_field_order_view(self):
        """
        Check that a custom form field ordering is in effect
        """
        response = self.client.get(reverse('admin:tests_kingdom_change', args=(1,)))

        self.assertEqual(response.status_code, 200)
        self.assertStringOrder(response, [
            '<th>Alive',
            '<th>Name',
            '<th>House'
        ])
