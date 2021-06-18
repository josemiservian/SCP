#Django
import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, RangeFilter

#Modelos
from apps.administracion.models import Gasto, Pago

class FacturacionFilter(django_filters.FilterSet):
    pass


class GastoFilter(django_filters.FilterSet):

    #motivo = CharFilter(field_name='motivo', label='Motivo', lookup_expr='icontains')
    #detalle = CharFilter(field_name='detalle', label='Detalle', lookup_expr='icontains')
    fecha_inicio = DateFilter(field_name='fecha', label='Fecha (Mayor/igual a)',lookup_expr='gte')
    fecha_fin = DateFilter(field_name='fecha', label='Fecha (Menor/igual a)',lookup_expr='lte')
    
    class Meta:
        model = Gasto
        fields = ('__all__')
        exclude = ['detalle','registro', 'fecha', 'gasto']


class PagoFilter(django_filters.FilterSet):

    monto_minimo = NumberFilter(field_name='monto', lookup_expr='gte')
    monto_maximo = NumberFilter(field_name='monto', lookup_expr='lte')
    detalle = CharFilter(field_name='detalle', lookup_expr='icontains')
    descripcion = CharFilter(field_name='descripcion', lookup_expr='icontains')
    fecha_inicio = DateFilter(field_name='fecha', lookup_expr='gte')
    fecha_fin = DateFilter(field_name='fecha', lookup_expr='lte')
    estado = django_filters.ChoiceFilter(choices=(('P', 'Pagado'), ('NP', 'No pagado')))

    class Meta:
        model = Pago
        #fields = ['estado']
        exclude = ['fecha', 'saldo', 'nro_cuota', 'detalle', 'descripcion', 'monto', 'estado']