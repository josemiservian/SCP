from django.urls import path
from apps.proyectos.views import clientes, contratos, equiposProyecto, registroHoras


urlpatterns = [
	
    #Clientes
    path(
        route='clientes/crear',
        view=clientes.crear_cliente,#CrearCliente.as_view(),
        name='clientes-crear'
    ),
    path(
        route='clientes/modificar/<str:pk>',
        view=clientes.actualizar_cliente,
        name='clientes-modificar'
    ),
    path(
        route='clientes/borrar/<str:pk>',
        view=clientes.borrar_cliente,
        name='clientes-borrar'
    ),
    path(
        route='clientes/listar',
        view=clientes.listar_clientes,
        name='clientes-listar'
    ),

    #Contratos
    path(
        route='contratos/crear',
        view=contratos.crear_contrato,#CrearContrato.as_view(),
        name='contratos-crear'
    ),
    path(
        route='contratos/modificar/<str:pk>',
        view=contratos.actualizar_contrato,
        name='contratos-modificar'
    ),
    path(
        route='contratos/borrar/<str:pk>',
        view=contratos.borrar_contrato,
        name='contratos-borrar'
    ),
    path(
        route='contratos/listar',
        view=contratos.listar_contratos,
        name='contratos-listar'
    ),
    #Equipos de Proyecto
    path(
        route='squads/crear',
        view=equiposProyecto.crear_equipo,#CrearEquipo.as_view(),
        name='squads-crear'
    ),
    path(
        route='squads/add/<str:pk>/',
        view=equiposProyecto.add_integrante,#AddMiembro.as_view(),
        name='squads-add'
    ),
    path(
        route='squads/modificar/<str:pk>',
        view=equiposProyecto.actualizar_equipo,
        name='squads-modificar'
    ),
    path(
        route='squads/borrar/<str:pk>',
        view=equiposProyecto.borrar_equipo,
        name='squads-borrar-equipo'
    ),
    path(
        route='squads/listar',
        view=equiposProyecto.listar_equipos,#ListaEquipos.as_view()
        name='squads-listar'
    ),
    path(
        route='squads/borrar-integrante/<str:pk>',
        view=equiposProyecto.borrar_integrante,
        name='squads-borrar-integrante'
    ),
    path(
        route='squads/<str:pk>/integrantes',
        view=equiposProyecto.listar_integrantes,
        name='squads-integrantes'
    ),
    #Registro de Horas
    path(
        route='registrohoras/crear',
        view=registroHoras.crear_registroHoras,
        name='registrohoras-crear'
    ),
    path(
        route='registrohoras/modificar/<str:pk>',
        view=registroHoras.actualizar_registroHora,
        name='registrohoras-modificar'
    ),
    path(
        route='registrohoras/borrar/<str:pk>',
        view=registroHoras.borrar_registroHora,
        name='registrohoras-borrar'
    ),
    #path(
    #    route='registrohoras/listar/<str:empleado__usuario__username>',#
    #    view=registroHoras.listar_registroHoras,
    #    name='registrohoras-listar'
    #),
    path(
        route='registrohoras/listar',
        view=registroHoras.listar_registroHoras,
        name='registrohoras-listar'
    ),
]