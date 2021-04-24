#Django
import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, RangeFilter

#Modelos
from apps.proyectos.models import RegistroHora

class RegistroHoraFilter(django_filters.FilterSet):
    
    nombre = CharFilter(field_name='nombre', label= 'Nombre', lookup_expr='icontains')
    detalle = CharFilter(field_name='nombre', label= 'Detalle', lookup_expr='icontains')
    fecha_inicio = DateFilter(field_name='fecha', label= 'Fecha (Mayor o igual)', lookup_expr='gte')
    fecha_fin = DateFilter(field_name='fecha', label= 'Fecha (Menor o igual)', lookup_expr='lte')
    
    class Meta:

        model = RegistroHora
        fields = ('__all__')
        exclude = [
            'empleado',
            'nombre', 
            'detalle',
            'hora_inicio', 
            'hora_fin', 
            'horas_trabajadas', 
            'fecha'
        ]
        