from django.test import TestCase
from django.urls import reverse


class BlogHomePageTests(TestCase):
    def test_root_url_shows_home_page_content(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'She went to the bank')
