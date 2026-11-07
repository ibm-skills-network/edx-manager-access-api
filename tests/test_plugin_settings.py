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


def test_leaves_the_setting_absent_when_the_environment_has_none(monkeypatch):
    # A plugin that runs later may check hasattr(settings, 'AUTH_USERNAME').
    monkeypatch.delenv('AUTH_USERNAME', raising=False)
    settings = SimpleNamespace()
    common.plugin_settings(settings)
    assert not hasattr(settings, 'AUTH_USERNAME')
