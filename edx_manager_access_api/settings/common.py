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
    if not getattr(settings, 'AUTH_USERNAME', None):
        settings.AUTH_USERNAME = os.environ.get('AUTH_USERNAME')
