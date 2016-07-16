from django.test import TestCase
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site


class AboutTestCase(TestCase):

    def setUp(self):
        site = Site.objects.get_current()
        f = FlatPage.objects.create(
            url="/about/", title="About")
        f.sites.add(site)

    def test_about__basic_request(self):
        resp = self.client.get('/about/')
        self.assertEqual(resp.status_code, 200)
