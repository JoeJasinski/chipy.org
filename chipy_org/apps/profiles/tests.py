"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfilesListTest(TestCase):

    def test_get__basic_request(self):
        resp = self.client.get('/profiles/list/')
        self.assertEqual(resp.status_code, 200)


class ProfilesEditTest(TestCase):

    def setUp(self):
        u = User.objects.create(username='joe')
        u.set_password('1234')
        u.save()
        self.user = u

    def test_get__annon_request(self):
        client = self.client
        resp = client.get('/profiles/edit/')
        self.assertEqual(resp.status_code, 302)

    def test_get__login_request(self):
        client = self.client
        client.login(username="joe", password="1234")
        resp = client.get('/profiles/edit/')
        self.assertEqual(resp.status_code, 200)
