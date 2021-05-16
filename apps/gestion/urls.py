from django.urls import path
from apps.gestion.views import areas, empleados, grupos, roles, servicios


urlpatterns = [
	
    #Areas
    path(
        route='areas/crear',
        view=areas.crear_area,
        name='areas-crear'
    ),
    path(
        route='areas/modificar/<str:pk>',
        view=areas.actualizar_area,
        name='areas-modificar'
    ),
    path(
        route='areas/borrar/<str:pk>',
        view=areas.borrar_area,
        name='areas-borrar'
    ),
    path(
        route='areas/listar',
        view=areas.listar_areas,
        name='areas-listar'
    ),

    #Gestión de Empleados
    path(
        route='empleados/crear',
        view=empleados.crear_empleado,
        name='empleados-crear'
    ),
    path(
        route='empleados/modificar/<str:pk>/',
        view=empleados.actualizar_empleado,
        name='empleados-modificar'
    ),
    path(
        route='empleados/listar',
        view=empleados.listar_empleados,
        name='empleados-listar'
    ),
    path(
        route='empleados/borrar/<str:pk>',
        view=empleados.borrar_empleado,
        name='empleados-borrar'
    ),
    #Grupos
    path(
        route='grupos/crear',
        view=grupos.crear_grupo,#Creargrupo.as_view(),
        name='grupos-crear'
    ),
    path(
        route='grupos/modificar/<str:pk>',
        view=grupos.actualizar_grupo,
        name='grupos-modificar'
    ),
    path(
        route='grupos/borrar/<str:pk>',
        view=grupos.borrar_grupo,
        name='grupos-borrar'
    ),
    path(
        route='grupos/listar',
        view=grupos.listar_grupos,
        name='grupos-listar'
    ),

    #Roles
    path(
        route='roles/crear',
        view=roles.crear_roles,#CrearRol.as_view(),
        name='roles-crear'
    ),
    path(
        route='roles/modificar/<str:pk>',
        view=roles.actualizar_rol,
        name='roles-modificar'
    ),
    path(
        route='borrar/<str:pk>',
        view=roles.borrar_rol,
        name='roles-borrar'
    ),
    path(
        route='roles/listar',
        view=roles.listar_roles,
        name='roles-listar'
    ),
     path(route='cargos/json/<str:pk>', view=roles.cargo_json),

    #Servicios
    path(
        route='servicios/crear',
        view=servicios.crear_servicio,#CrearServicio.as_view(),
        name='servicios-crear'
    ),
    path(
        route='servicios/modificar/<str:pk>',
        view=servicios.actualizar_servicio,
        name='servicios-modificar'
    ),
    path(
        route='servicios/borrar/<str:pk>',
        view=servicios.borrar_servicio,
        name='servicios-borrar'
    ),
    path(
        route='servicios/listar',
        view=servicios.listar_servicios,
        name='servicios-listar'
    ),
]