"""
edx_manager_access_api Django application initialization.
"""

from django.apps import AppConfig


class EdxManagerAccessApiConfig(AppConfig):
    """
    Configuration for the edx_manager_access_api Django application.
    """

    name = 'edx_manager_access_api'
    plugin_app = {
        'url_config': {
            'lms.djangoapp': {
                'namespace': 'edx_manager_access_api',
                'regex': r'^sn-api/manager-access/',
            },
        },
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
            },
        },
    }
