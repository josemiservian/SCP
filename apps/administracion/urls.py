from django.urls import path
from apps.administracion.views import facturaciones, pagos


urlpatterns = [
	
    #facturaciones
    path(
        route='facturaciones/crear',
        view=facturaciones.crear_factura,#CrearFactura.as_view(),
        name='facturaciones-crear'
    ),
    path(
        route='facturaciones/modificar/<str:pk>',
        view=facturaciones.actualizar_factura,
        name='facturaciones-modificar'
    ),
    path(
        route='facturaciones/borrar/<str:pk>',
        view=facturaciones.borrar_factura,
        name='facturaciones-borrar'
    ),
    path(
        route='facturaciones/listar',
        view=facturaciones.listar_facturas,
        name='facturaciones-listar'
    ),

    #Pagos
    path(
        route='pagos/crear',
        view=pagos.crear_pago,#CrearPago.as_view(),
        name='pagos-crear'
    ),
    path(
        route='pagos/modificar/<str:pk>',
        view=pagos.actualizar_pago,
        name='pagos-modificar'
    ),
    path(
        route='pagos/borrar/<str:pk>',
        view=pagos.borrar_pago,
        name='pagos-borrar'
    ),
    path(
        route='pagos/listar',
        view=pagos.listar_pagos,
        name='pagos-listar'
    ),
]