import datetime
from django.test import TestCase, override_settings
from django.test import Client
from django.core.urlresolvers import reverse_lazy
from django.conf import global_settings
from django.contrib.auth import get_user_model

import chipy_org.libs.test_utils as test_utils
from .models import RSVP, Meeting, Venue, Topic, Topic

User = get_user_model()


class MeetingsTest(test_utils.AuthenticatedTest):
    def test_unique_rsvp(self):
        """
        Tests the uniqueness constraints on the rsvp model
        """

        from django.core.exceptions import ValidationError

        test_venue = Venue.objects.create(name='Test')
        meeting = Meeting.objects.create(
            when=datetime.date.today(), where=test_venue)
        rsvp = RSVP.objects.create(
            user=self.user, meeting=meeting, response='Y')

        with self.assertRaises(ValidationError):
            # RSVP needs to have a user or name
            rsvp_no_user = RSVP.objects.create(
                meeting=meeting, response='Y')

        with self.assertRaises(ValidationError):
            # This should already exist
            duplicate_rsvp = RSVP.objects.create(
                user=self.user, meeting=meeting, response='Y')

        with self.assertRaises(ValidationError):
            name_rsvp = RSVP.objects.create(
                name='Test Name', meeting=meeting,
                response='Y', email='dummy@example.com',
            )

            # Can't have two of the same name
            duplicate_name_rsvp = RSVP.objects.create(
                name='Test Name', meeting=meeting,
                response='Y', email='dummy@example.com',
            )


@override_settings(
    STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
class SmokeTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="chipy",)
        self.meeting = Meeting.objects.create(
            when=datetime.datetime.now() + datetime.timedelta(days=7)
        )
        self.topic = Topic.objects.create(
            title="test topic"
        )

    def test__past_meetings__GET(self):
        # TEST
        response = self.client.get(reverse_lazy('past_meetings'))

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__meeting_detail__GET(self):
        # TEST
        response = self.client.get(
            reverse_lazy('meeting', args=[self.meeting.id]))

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__propose_topic__GET__annon(self):
        # TEST
        response = self.client.get(reverse_lazy('propose_topic'))

        # CHECK
        self.assertEqual(response.status_code, 302)

    def test__propose_topic__POST__annon(self):
        # TEST
        response = self.client.post(reverse_lazy('propose_topic'))

        # CHECK
        self.assertEqual(response.status_code, 302)

    def test__propose_topic__GET__auth(self):
        # SETUP
        self.client.force_login(self.user)

        # TEST
        response = self.client.get(reverse_lazy('propose_topic'))

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__propose_topic__POST__auth__error(self):
        # SETUP
        self.client.force_login(self.user)

        # TEST
        response = self.client.post(reverse_lazy('propose_topic'))

        # CHECK
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(
            set(response.context['form'].errors.as_data().keys()),
            set({'email', 'title', 'experience_level',
                 'name', 'description', 'license'})
        )

    def test__propose_topic__POST__auth__success(self):
        # SETUP
        self.client.force_login(self.user)
        title = "Example Title"
        description = "test desc"
        experience_level = "novice"
        license = "CC BY"
        name = "test testerson"
        email = "test@example.com"

        # TEST
        response = self.client.post(
            reverse_lazy('propose_topic'),
            data={
                "name": name,
                "email": email,
                "title": title,
                "experience_level": experience_level,
                "description": description,
                "license": license, }
            )

        # CHECK
        self.assertEqual(response.status_code, 302)
        t = Topic.objects.last()
        self.assertEqual(t.title, title)
        self.assertEqual(Topic.objects.count(), 2)
        self.assertEqual(t.description, description)
        self.assertEqual(t.experience_level, experience_level)
        self.assertEqual(t.license, license)
        self.assertEqual(t.presentors.count(), 1)
        self.assertEqual(t.presentors.first().name, name)
        self.assertEqual(t.presentors.first().email, email)

    def test__past_topics__GET(self):
        # TEST
        response = self.client.get(reverse_lazy('past_topics'))

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__past_topic__GET(self):
        # TEST
        response = self.client.get(
            reverse_lazy('past_topic', args=[self.topic.id]))

        # CHECK
        self.assertEqual(response.status_code, 200)
