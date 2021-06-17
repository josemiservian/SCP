from django.urls import path

from apps.consultas.vistas.c_contrato import ConsultaView

urlpatterns = [
    # reports
    path('c_contratos/', ConsultaView.as_view(), name='c_contrato'),
]