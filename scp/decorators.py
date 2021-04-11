from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group

def allowed_users(action):
    '''Decorador para verificar si el rol puede proceder a realizar la acción solicitada. '''

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in Group.objects.filter(permissions__codename=action).values_list('name', flat=True):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No esta autorizado para ver esta pagina')
                #raise PermissionDenied
        return wrapper_func
    return decorator

def funcion(user):
    '''Decorador para restringir de que un usuario vea datos de otro usuarios. '''

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in Group.objects.filter(permissions__codename=action).values_list('name', flat=True):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No esta autorizado para ver esta pagina')
                #raise PermissionDenied
        return wrapper_func
    return decorator