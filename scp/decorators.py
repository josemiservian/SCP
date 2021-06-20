from django.http import HttpResponse
from django.contrib.auth.models import Group

#Modelos
from apps.cuentas.models import Empleado
from apps.proyectos.models import EquipoProyecto, MiembroEquipoProyecto

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

def validar_empleado_proyecto():
    '''Decorador para validar que el usuario esté asociado a un proyecto para la carga de horas.'''
    
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            empleado = Empleado.objects.get(usuario__username=request.user)
            if MiembroEquipoProyecto.objects.filter(empleado=empleado) or EquipoProyecto.objects.filter(lider_proyecto=empleado):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Usted no está asociado a ningún proyecto.')
        return wrapper_func
    return decorator