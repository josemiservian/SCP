from django.urls import path

from apps.consultas.vistas.c_contrato import ConsultaView
from apps.consultas.vistas.graficos import GraficoView

urlpatterns = [
    # reports
    path('c_contratos/', ConsultaView.as_view(), name='c_contrato'),

    #grafico
    path('c_contratos/graficos', GraficoView.as_view(), name='graficos'),
    #path('graficos', GraficoView.as_view(), name='graficos'),
]