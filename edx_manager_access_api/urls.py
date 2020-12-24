"""
URLs for edx_manager_access_api.
"""
from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^access$', views.ManagerAccessView.as_view(), name='manager_access'),
]
