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
        route='configuracion',
        view=empleados.VistaActualizarPerfil.as_view(),
        name='configuracion'
    ),
]