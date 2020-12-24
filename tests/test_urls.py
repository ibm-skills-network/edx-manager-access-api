#!/usr/bin/env python
"""
Tests for the `edx-manager-access-api` models module.
"""

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from edx_manager_access_api.views import ManagerAccessView


class TestUrls(SimpleTestCase):
    """
    Test that URLs are mapped to the correct views
    """
    def test_manager_enabled(self):
        url = reverse('manager_access')
        self.assertEqual(resolve(url).func.view_class, ManagerAccessView)
