import os

def plugin_settings(settings):
    """
    Modify the provided settings object with settings specific to this plugin.
    """
    settings.BASICAUTH_USERS = {
        os.environ.get('AUTH_USERNAME'): os.environ.get('AUTH_PASSWORD'),
        'key': 'secret'
    }
