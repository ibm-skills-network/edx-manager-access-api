"""
Tests for the plugin settings the LMS applies at startup.
"""
from types import SimpleNamespace

from edx_manager_access_api.settings import common


def test_reads_the_service_username_from_the_environment(monkeypatch):
    monkeypatch.setenv('AUTH_USERNAME', 'svc-test')
    settings = SimpleNamespace()
    common.plugin_settings(settings)
    assert settings.AUTH_USERNAME == 'svc-test'


def test_keeps_a_service_username_another_plugin_set(monkeypatch):
    # The LMS runs every plugin's plugin_settings on one settings object.
    monkeypatch.setenv('AUTH_USERNAME', 'svc-env')
    settings = SimpleNamespace(AUTH_USERNAME='svc-sibling')
    common.plugin_settings(settings)
    assert settings.AUTH_USERNAME == 'svc-sibling'
