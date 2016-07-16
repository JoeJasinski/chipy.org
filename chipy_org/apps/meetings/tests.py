import datetime

import chipy_org.libs.test_utils as test_utils
from .models import RSVP, Meeting, Venue, Topic
from django.test import TestCase


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


class IcalDownloadTest(TestCase):

    def test_get__annon_request(self):
        client = self.client
        resp = client.get('/meetings/ical/')
        self.assertEqual(resp.status_code, 200)


class PastMeetingsTest(TestCase):

    def setUp(self):
        super(PastMeetingsTest, self).setUp()
        self.meeting = Meeting.objects.create(
            when=datetime.datetime(2016, 1, 1, 0, 0),
            key="123")
        self.meeting_future = Meeting.objects.create(
            when=datetime.datetime(
                datetime.datetime.now().year + 1, 1, 1, 0, 0))

    def test_get__only_past_meetings(self):
        client = self.client
        resp = client.get('/meetings/past/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context_data['meeting_list']), 1)
        meeting = resp.context_data['meeting_list'][0]
        self.assertEqual(meeting.id, self.meeting.id)


class RSVPTest(test_utils.AuthenticatedTest):

    def setUp(self):
        super(RSVPTest, self).setUp()
        self.meeting = Meeting.objects.create(
            when=datetime.datetime(2016, 1, 1, 0, 0))

    def test_rsvp__annon_request(self):
        client = self.client
        resp = client.get('/meetings/rsvp/')
        self.assertEqual(resp.status_code, 200)

    def test_rsvp_anonymous__annon_request(self):
        client = self.client
        resp = client.get('/meetings/rsvp/anonymous/')
        self.assertEqual(resp.status_code, 200)

    def test_rsvp_anonymous_rsvp_key__auth_request(self):
        client = self.c  # authenticted client
        rsvp = RSVP.objects.create(
            meeting=self.meeting,
            key="1234567890123456789012345678901234567890",
            response="Y",
            user=self.user,
        )
        resp = client.get('/meetings/rsvp/anonymous/{}/'.format(
            rsvp.key
        ))
        self.assertEqual(resp.status_code, 200)


class TopicsProposeTest(test_utils.AuthenticatedTest):

    def test_topics_propose__annon_request(self):
        client = self.client
        resp = client.get('/meetings/topics/propose/')
        self.assertEqual(resp.status_code, 302)

    def test_topics_propose__authenticated_request(self):
        client = self.c  # use the "c" client which is authenticated
        resp = client.get('/meetings/topics/propose/')
        self.assertEqual(resp.status_code, 200)


class TopicsMineTest(test_utils.AuthenticatedTest):

    def test_topics_mine__annon_request(self):
        client = self.client
        resp = client.get('/meetings/topics/mine/')
        self.assertEqual(resp.status_code, 302)

    def test_topics_mine__authenticated_request(self):
        client = self.c  # use the "c" client which is authenticated
        resp = client.get('/meetings/topics/mine/')
        self.assertEqual(resp.status_code, 200)


class TopicsPastTest(test_utils.AuthenticatedTest):

    def setUp(self):
        super(TopicsPastTest, self).setUp()
        self.meeting = Meeting.objects.create(
            when=datetime.datetime(2016, 1, 1, 0, 0))
        self.topic1 = Topic.objects.create(
            title='approved_topic', meeting=self.meeting, approved=True)
        self.topic2 = Topic.objects.create(
            title='unapproved_topic', meeting=self.meeting, approved=False)

    def test_topics_past__annon_request(self):
        client = self.client
        resp = client.get('/meetings/topics/past/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(1, len(resp.context_data['topics']))

    def test_topics_past__authenticated_request(self):
        client = self.c  # use the "c" client which is authenticated
        resp = client.get('/meetings/topics/past/')
        self.assertEqual(resp.status_code, 200)

    def test_topics_past__annon_request_approved(self):
        client = self.client
        resp = client.get('/meetings/topics/past/')
        self.assertEqual(resp.status_code, 200)
        topic = resp.context_data['topics'][0]
        self.assertEqual(len(resp.context_data['topics']), 1)
        self.assertTrue(topic.approved)
        self.assertEqual(topic.title, "approved_topic")

    def test_topic_past_id__approved_topic(self):
        client = self.client
        resp = client.get('/meetings/topics/past/{}/'.format(self.topic1.pk))
        self.assertEqual(resp.status_code, 200)
        topic = resp.context_data['topic']
        self.assertEqual(topic.title, "approved_topic")
