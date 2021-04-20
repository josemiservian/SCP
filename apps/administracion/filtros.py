#Django
import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, RangeFilter

#Modelos
from .models import *

class FacturacionFilter(django_filters.FilterSet):
    pass


class GastoFilter(django_filters.FilterSet):

    fecha_inicio = DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_fin = DateFilter(field_name='fecha', lookup_expr='lte')
    motivo = CharFilter(field_name='motivo', lookup_expr='icontains')
    
    class Meta:
        model = Gasto
        fields = ('__all__')
        exclude = ['registro']


class PagoFilter(django_filters.FilterSet):

    monto_minimo = NumberFilter(field_name='monto', lookup_expr='gte')
    monto_maximo = NumberFilter(field_name='monto', lookup_expr='lte')
    detalle = CharFilter(field_name='detalle', lookup_expr='icontains')
    descripcion = CharFilter(field_name='descripcion', lookup_expr='icontains')
    fecha_inicio = DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_fin = DateFilter(field_name='fecha', lookup_expr='lte')

    class Meta:
        model = Pago
        fields = ('__all__')
        exclude = ['fecha', 'saldo', 'nro_cuota', 'detalle', 'descripcion', 'monto']