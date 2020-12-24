from .utils import extract_manager
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import View

from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from basicauth.decorators import basic_auth_required
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(basic_auth_required, name='dispatch')
class ManagerAccessView(View):
    """
    Provides functionality to interact with EdX staff and superuser access
    """
    def post(self, request):
        """
        Enables a manager to have studio and django access
        body params
            - email
        """
        try:
            manager = extract_manager(request)
        except KeyError:
            return HttpResponseBadRequest('Missing email')

        manager.is_staff = True
        manager.is_superuser = True
        manager.save()
        return JsonResponse({'message': '{manager_email} is now able to access Studio and the Django Admin Console.'.format(manager_email=manager.email)})

    def delete(self, request):
        """
        Removes a manager from having studio and django access
        body params
            - email
        """
        try:
            manager = extract_manager(request)
        except KeyError:
            return HttpResponseBadRequest('Missing email')

        manager.is_staff = False
        manager.is_superuser = False
        manager.save()
        return JsonResponse({'message': '{manager_email} is no longer able to access Studio and the Django Admin Console.'.format(manager_email=manager.email)})
