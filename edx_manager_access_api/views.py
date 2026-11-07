import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth.models import User

from .permissions import IsServiceAccount

log = logging.getLogger(__name__)


class GrantManagerAccessView(APIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsServiceAccount]

    def post(self, request):
        """
        Enables a manager to have studio and django access
        body params
            - email
        """
        email = request.data.get("email", None)
        if not email:
            msg = {"error": "Missing parameter 'email' in body."}
            log.info(msg)
            raise ParseError(msg)

        try:
            manager = User.objects.get(email=email)
        except Exception:  # pylint: disable=broad-except
            msg = {
                "error": "Could not find user by email address '{email}'".format(
                    email=email
                )
            }
            return Response(msg, 404)

        manager.is_staff = True
        manager.is_superuser = True
        manager.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RevokeManagerAccessView(APIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, IsServiceAccount]

    def post(self, request):
        """
        Removes a manager from having studio and django access
        body params
            - email
        """
        email = request.data.get("email", None)
        if not email:
            msg = {"error": "Missing parameter 'email' in body."}
            log.info(msg)
            raise ParseError(msg)

        try:
            manager = User.objects.get(email=email)
        except Exception:  # pylint: disable=broad-except
            msg = {
                "error": "Could not find user by email address '{email}'".format(
                    email=email
                )
            }
            return Response(msg, 404)

        # Every Skills Network plugin admits only the staff account named by
        # AUTH_USERNAME. Taking staff away from it locks all of them out.
        if manager.username == settings.AUTH_USERNAME:
            msg = {"error": "The service account's own access cannot be revoked."}
            log.warning(msg)
            raise ParseError(msg)

        manager.is_staff = False
        manager.is_superuser = False
        manager.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
