from django.test import TestCase, Client
from unittest import mock
from django.urls import reverse
from django.test.utils import override_settings
from django.contrib.auth.models import User

import json

USERNAME = 'user'
EMAIL = 'test@place.com'
PASSWORD = 'pass123'

def serialize(d):
    """
    Serialize a dict as a json string. To be used in client requests
    """
    return json.dumps(d)

class MixinTests(object):
    """
    Make our tests DRY by putting common tests here
    we can then inherit this class to add a full test suite
    Each test tests behaviour of BOTH POST/DELETE methods so as to not repeat test definitions
    POST == Enable access to studio and django
    DELETE == Disable access to studio and django
    """
    @override_settings(BASICAUTH_DISABLE=False) # rather than mocking auth, we disable it in `test_settings.py`
    def test__fails_without_auth(self):
        """
        Rather than mocking auth, we disable it in `test_settings.py`,
        for this test we want to mimick authentication failing so we
        override the BASICAUTH_DISABLE to be false for this test
        """
        # Enable
        res = self.client.post(self.url, serialize(self.body), content_type="application/json")
        self.assertEqual(res.status_code, 401)
        # Disable
        res = self.client.delete(self.url, serialize(self.body), content_type="application/json")
        self.assertEqual(res.status_code, 401)

    def test__400_missing_param(self):
        # Enable
        # without email
        body = dict(self.body)
        del body['email']
        res = self.client.post(self.url, serialize(body), content_type="application/json")
        self.assertEqual(res.status_code, 400)
        # Unenroll
        # email
        body = dict(self.body)
        del body['email']
        res = self.client.delete(self.url, serialize(body), content_type="application/json")
        self.assertEqual(res.status_code, 400)

    def test__404_missing_user(self):
        body = {
            'email': 'incorrect'+EMAIL,
        }
        # Enable
        res = self.client.post(self.url, serialize(body), content_type="application/json")
        self.assertEqual(res.status_code, 404)
        # Disable
        res = self.client.delete(self.url, serialize(body), content_type="application/json")
        self.assertEqual(res.status_code, 404)

    def test__success(self):
        # Enable
        res = self.client.post(self.url, serialize(self.body), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn(res.json()['message'], '{manager_email} is now able to access Studio and the Django Admin Console.'.format(manager_email=self.body['email'])})
        # Disable
        res = self.client.delete(self.url, serialize(self.body), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn(res.json()['message'], '{manager_email} is no longer able to access Studio and the Django Admin Console.'.format(manager_email=self.body['email'])})

    def test__405(self):
        res = self.client.patch(self.url, serialize(self.body), content_type="application/json")
        self.assertEqual(res.status_code, 405)
        res = self.client.put(self.url, serialize(self.body), content_type="application/json")
        self.assertEqual(res.status_code, 405)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 405)

class TestManagerAccessView(MixinTests, TestCase):
    def setUp(self):
        """
        initialize an environment for the below tests
        """
        self.client = Client()
        self.user = User.objects.create_user(USERNAME, EMAIL, PASSWORD)
        self.url = reverse('manager_access')
        self.body = {
            'email': EMAIL,
        }
