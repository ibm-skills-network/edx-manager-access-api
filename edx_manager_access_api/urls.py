"""
URLs for edx_manager_access_api.
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^grant_access$', views.GrantManagerAccessView.as_view(), name='grant_manager_access'),
    url(r'^revoke_access$', views.RevokeManagerAccessView.as_view(), name='revoke_manager_access'),
]
