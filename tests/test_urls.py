#!/usr/bin/env python
"""
Tests for the `edx-manager-access-api` URL routing.
"""

from django.test import SimpleTestCase
from django.urls import resolve, reverse

from edx_manager_access_api.views import GrantManagerAccessView, RevokeManagerAccessView


class TestUrls(SimpleTestCase):
    """
    Test that URLs are mapped to the correct views.
    """

    def test_grant_access_url(self):
        url = reverse('grant_manager_access')
        self.assertEqual(resolve(url).func.view_class, GrantManagerAccessView)

    def test_revoke_access_url(self):
        url = reverse('revoke_manager_access')
        self.assertEqual(resolve(url).func.view_class, RevokeManagerAccessView)
