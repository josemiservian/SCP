from django.urls import path
from apps.cuentas.views import empleados


urlpatterns = [
    #Empleados
    path(
        route='', 
        view=empleados.inicio, 
        name="inicio"
    ),
    path(
        route='admin', 
        view=empleados.admin, 
        name="admin"
    ),
    path(
        route='login',
        view=empleados.vista_login,
        name='login'
    ),
    path(
        route='logout',
        view=empleados.vista_logout,
        name='logout'
    ),
    path(
        route='configuracion/<str:username>',
        view=empleados.actualizar_perfil,
        name='configuracion'
    ),
    path(
        route='perfil/<str:username>',
        view=empleados.ver_perfil,
        name='perfil'
    )
]