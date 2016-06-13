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
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username='super', 
            password='secret', 
            email='super@example.com'
        )

        # Basic Test data
        cls.author = Author.objects.create(name="William Shakespeare")

        cls.play1 = Play.objects.create(
            title='Romeo and Juliet', genre='Tragedy',
            year=1597, author=cls.author, id=1)
        cls.play2 = Play.objects.create(
            title="A Midsummer Night's Dream", genre='Comedy',
            year=1600, author=cls.author, id=3)
        cls.play3 = Play.objects.create(
            title='Julius Caesar', genre='Tragedy',
            year=1623, author=cls.author, id=5)
        

        cls.poem1 = Poem.objects.create(
            title="Shall I compare thee to a summer's day?",
            style="Sonnet", author=cls.author, id=2)
        cls.poem2 = Poem.objects.create(
            title="As a decrepit father takes delight",
            style="Sonnet", author=cls.author, id=4)

        # Custom order field 
        cls.westeros = Kingdom.objects.create(name="Westeros")

        cls.king1 = King.objects.create(
            kingdom=cls.westeros, name="Tommen Baratheon", alive=True, id=1)
        cls.king2 = King.objects.create(
            kingdom=cls.westeros, name="Joffrey Baratheon", alive=False, id=2)
        cls.king3 = King.objects.create(
            kingdom=cls.westeros, name="Rob Stark", alive=False, id=3)

        cls.soldier1 = Soldier.objects.create(
            kingdom=cls.westeros, name="The Hound", house="Brotherhood Without Banners", id=1)
        cls.soldier1 = Soldier.objects.create(
            kingdom=cls.westeros, name="Bronn", house="Lannister?", id=2)

    def setUp(self):
        self.client.force_login(self.superuser)

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

        response = self.client.get('/admin/tests/author/1/change/') 

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

        response = self.client.get('/admin/tests/kingdom/1/change/')

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
        response = self.client.get('/admin/tests/kingdom/1/change/')

        self.assertEqual(response.status_code, 200)
        self.assertStringOrder(response, [
            '<th>Alive',
            '<th>Name',
            '<th>House'
        ])
