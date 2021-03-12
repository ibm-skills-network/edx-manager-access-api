import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

log = logging.getLogger(__name__)


class GrantManagerAccessView(APIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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

        manager.is_staff = False
        manager.is_superuser = False
        manager.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
