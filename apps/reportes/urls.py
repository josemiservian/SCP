from django.urls import path
from apps.reportes.views import seguimientos
from apps.reportes.views import reporte

urlpatterns = [
	
    path(
        route='seguimientos/report',
        view= reporte.ReportHorasView.as_view(),
        #ReportHorasView.as_view(),
        name='Report-Horas'
    ),
    path(
        route='seguimientos/crear',
        view=seguimientos.crear_seguimiento,#CrearSeguimiento.as_view(),
        name='seguimientos-crear'
    ),
    path(
        route='seguimientos/modificar/<str:pk>',
        view=seguimientos.actualizar_seguimiento,
        name='seguimientos-modificar'
    ),
    path(
        route='seguimientos/borrar/<str:pk>',
        view=seguimientos.borrar_seguimiento,
        name='seguimientos-borrar'
    ),
    path(
        route='seguimientos/listar',
        view=seguimientos.listar_seguimientos,
        name='seguimientos-listar'
    ),
]