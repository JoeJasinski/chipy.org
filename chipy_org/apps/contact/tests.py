from django.test import TestCase


class ChipyContactViewTestCase(TestCase):

    def test_contact__basic_request(self):
        resp = self.client.get('/contact/')
        self.assertEqual(resp.status_code, 200)
