"""
See apps.py for details on how this sort of plugin configures itself for
integration with Open edX.
"""

import os


def plugin_settings(settings):
    """
    Modify the provided settings object with settings specific to this plugin.
    """
    # IsServiceAccount reads AUTH_USERNAME. The other Skills Network plugins in the
    # LMS set it from the same environment variable. This plugin reads it too, so
    # its endpoints do not depend on one of them being installed.
    # With the variable unset it leaves the setting alone. Writing None would make
    # hasattr() true for a plugin whose plugin_settings runs after this one.
    username = os.environ.get('AUTH_USERNAME')
    if username and not getattr(settings, 'AUTH_USERNAME', None):
        settings.AUTH_USERNAME = username
