import os
import base64
from django.http import HttpResponse
from django.conf import settings


def basicauth(view):
    def wrap(request, *args, **kwargs):
        user = settings.AUTH_USERNAME
        password = settings.AUTH_PASSWORD
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).decode("utf8").split(':')
                    if uname == user and passwd == password:
                        return view(request, *args, **kwargs)

        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="api"'
        return response
    return wrap