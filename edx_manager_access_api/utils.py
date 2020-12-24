import json
from django.contrib.auth.models import User
from django.http import Http404

def extract_manager(request):
    """
    Extract the manager email from the request body
    """
    body = json.loads(request.body)
    manager_email = body['email']
    manager = User.objects.filter(email=manager_email)

    if manager.exists():
        return manager.first()

    raise Http404('User not found')
