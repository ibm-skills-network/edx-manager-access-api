#!/usr/bin/env python
"""
Tests for the `edx-manager-access-api` views module.

These exercise the real authentication (HTTP Basic Auth) and authorization
(service-account only) behaviour of the grant/revoke endpoints, including a
regression test proving that neither an ordinary learner nor an unrelated
superuser can escalate privileges (HackerOne #3868326). Only the configured
``AUTH_USERNAME`` service account may call these endpoints.
"""

import base64
import json

from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import reverse

# Must match AUTH_USERNAME in test_settings.py.
SERVICE_USERNAME = 'sn-service'
SERVICE_EMAIL = 'service@place.com'
SERVICE_PASSWORD = 'servicepass123'

# A superuser that is NOT the service account -- must still be rejected.
ADMIN_USERNAME = 'other-admin'
ADMIN_EMAIL = 'other-admin@place.com'
ADMIN_PASSWORD = 'adminpass123'

LEARNER_USERNAME = 'learner'
LEARNER_EMAIL = 'learner@place.com'
LEARNER_PASSWORD = 'learnerpass123'

TARGET_USERNAME = 'target'
TARGET_EMAIL = 'target@place.com'
TARGET_PASSWORD = 'targetpass123'


def serialize(body):
    """Serialize a dict as a JSON string, to be used in client requests."""
    return json.dumps(body)


def basic_auth(username, password):
    """Build an HTTP Basic Auth header value for the given credentials."""
    token = base64.b64encode(
        '{username}:{password}'.format(username=username, password=password).encode()
    ).decode()
    return 'Basic {token}'.format(token=token)


class ManagerAccessTestMixin(object):
    """
    Shared authorization/validation tests for both the grant and revoke views.

    Subclasses must set ``self.url`` (after calling ``super().setUp()``).
    """

    def setUp(self):
        self.client = Client()
        self.service_account = User.objects.create_user(
            SERVICE_USERNAME, SERVICE_EMAIL, SERVICE_PASSWORD, is_staff=True
        )
        self.other_admin = User.objects.create_superuser(
            ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
        )
        self.learner = User.objects.create_user(
            LEARNER_USERNAME, LEARNER_EMAIL, LEARNER_PASSWORD
        )
        self.target = User.objects.create_user(
            TARGET_USERNAME, TARGET_EMAIL, TARGET_PASSWORD
        )
        self.body = {'email': TARGET_EMAIL}

    def post(self, credentials=None, body=None):
        """POST to the view under test, optionally authenticated via Basic Auth."""
        kwargs = {'content_type': 'application/json'}
        if credentials is not None:
            kwargs['HTTP_AUTHORIZATION'] = basic_auth(*credentials)
        payload = self.body if body is None else body
        return self.client.post(self.url, serialize(payload), **kwargs)

    def assert_target_unchanged(self, is_staff, is_superuser):
        """Assert the target user's privilege flags were not modified."""
        self.target.refresh_from_db()
        self.assertEqual(self.target.is_staff, is_staff)
        self.assertEqual(self.target.is_superuser, is_superuser)

    def test_requires_authentication(self):
        res = self.post()
        self.assertEqual(res.status_code, 401)

    def test_forbidden_for_learner(self):
        """Core regression: an authenticated non-staff learner is rejected."""
        before = (self.target.is_staff, self.target.is_superuser)
        res = self.post(credentials=(LEARNER_USERNAME, LEARNER_PASSWORD))
        self.assertEqual(res.status_code, 403)
        self.assert_target_unchanged(*before)

    def test_forbidden_for_non_service_superuser(self):
        """Even a real superuser is rejected unless it is the service account."""
        before = (self.target.is_staff, self.target.is_superuser)
        res = self.post(credentials=(ADMIN_USERNAME, ADMIN_PASSWORD))
        self.assertEqual(res.status_code, 403)
        self.assert_target_unchanged(*before)

    @override_settings(AUTH_USERNAME=LEARNER_USERNAME)
    def test_forbidden_when_username_matches_but_not_staff(self):
        """The is_staff clause blocks a username match on a non-staff account.

        Guards against username squatting: with open registration an attacker
        could self-register the configured service-account username, so matching
        the name must not be sufficient without staff status.
        """
        before = (self.target.is_staff, self.target.is_superuser)
        res = self.post(credentials=(LEARNER_USERNAME, LEARNER_PASSWORD))
        self.assertEqual(res.status_code, 403)
        self.assert_target_unchanged(*before)

    @override_settings(AUTH_USERNAME='')
    def test_fails_closed_when_service_account_unset(self):
        """If AUTH_USERNAME is not configured, even the service account is denied."""
        before = (self.target.is_staff, self.target.is_superuser)
        res = self.post(credentials=(SERVICE_USERNAME, SERVICE_PASSWORD))
        self.assertEqual(res.status_code, 403)
        self.assert_target_unchanged(*before)

    def test_400_missing_email(self):
        res = self.post(credentials=(SERVICE_USERNAME, SERVICE_PASSWORD), body={})
        self.assertEqual(res.status_code, 400)

    def test_404_missing_user(self):
        res = self.post(
            credentials=(SERVICE_USERNAME, SERVICE_PASSWORD),
            body={'email': 'nobody@place.com'},
        )
        self.assertEqual(res.status_code, 404)

    def test_405_wrong_methods(self):
        auth = basic_auth(SERVICE_USERNAME, SERVICE_PASSWORD)
        self.assertEqual(self.client.get(self.url, HTTP_AUTHORIZATION=auth).status_code, 405)
        for method in (self.client.put, self.client.patch, self.client.delete):
            res = method(
                self.url, serialize(self.body),
                content_type='application/json', HTTP_AUTHORIZATION=auth,
            )
            self.assertEqual(res.status_code, 405)


class TestGrantManagerAccessView(ManagerAccessTestMixin, TestCase):
    """Tests for GrantManagerAccessView."""

    def setUp(self):
        super().setUp()
        self.url = reverse('grant_manager_access')

    def test_grant_success_as_service_account(self):
        res = self.post(credentials=(SERVICE_USERNAME, SERVICE_PASSWORD))
        self.assertEqual(res.status_code, 204)
        self.target.refresh_from_db()
        self.assertTrue(self.target.is_staff)
        self.assertTrue(self.target.is_superuser)


class TestRevokeManagerAccessView(ManagerAccessTestMixin, TestCase):
    """Tests for RevokeManagerAccessView."""

    def setUp(self):
        super().setUp()
        self.url = reverse('revoke_manager_access')
        # Target starts privileged so we can observe revocation.
        self.target.is_staff = True
        self.target.is_superuser = True
        self.target.save()

    def test_revoke_success_as_service_account(self):
        res = self.post(credentials=(SERVICE_USERNAME, SERVICE_PASSWORD))
        self.assertEqual(res.status_code, 204)
        self.target.refresh_from_db()
        self.assertFalse(self.target.is_staff)
        self.assertFalse(self.target.is_superuser)
