"""
URLs for edx_manager_access_api.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('grant_access', views.GrantManagerAccessView.as_view(), name='grant_manager_access'),
    path('revoke_access', views.RevokeManagerAccessView.as_view(), name='revoke_manager_access'),
]
