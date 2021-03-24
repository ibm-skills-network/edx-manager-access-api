"""
URLs for edx_manager_access_api.
"""
from django.conf import settings
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^grant_access$', views.GrantManagerAccessView.as_view(), name='grant_manager_access'),
    url(r'^revoke_access$', views.RevokeManagerAccessView.as_view(), name='revoke_manager_access'),
]

# Since urls.py is executed once, create service user here for server to server auth
from django.contrib.auth.models import User
try:
    User.objects.get(username=settings.AUTH_USERNAME)
except User.DoesNotExist:
    User.objects.create_user(username=settings.AUTH_USERNAME,
                                    email=settings.EMAIL,
                                    password=settings.AUTH_PASSWORD, is_staff=True)
