#Django
import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter

#Modelos
from apps.proyectos.models import Contrato, RegistroHora, Propuesta, EquipoProyecto, Cliente

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


class ContratoFilter(django_filters.FilterSet):

    nombre = CharFilter(field_name='nombre', label= 'Nombre', lookup_expr='icontains')

    class Meta:
        model = Contrato
        fields =  ['cliente', 'propuesta', 'tipo_servicio']#('__all__')
        #exclude = ['nombre', 'created', 'modified', 'rentabilidad_presupuesto', 'descripcion', 'monto']


class PropuestaFilter(django_filters.FilterSet):

    nombre = CharFilter(field_name='nombre', label= 'Nombre', lookup_expr='icontains')

    class Meta:
        model = Propuesta
        fields =  ['area', 'estado']#('__all__')
        #exclude = ['nombre', 'created', 'modified', 'rentabilidad_presupuesto', 'descripcion', 'monto']


class EquipoProyectoFilter(django_filters.FilterSet):

    nombre = CharFilter(field_name='nombre', label= 'Nombre', lookup_expr='icontains')

    class Meta:
        model = EquipoProyecto
        fields =  ['contrato', 'lider_proyecto']#('__all__')
        #exclude = ['nombre', 'created', 'modified', 'rentabilidad_presupuesto', 'descripcion', 'monto']


class ClienteFilter(django_filters.FilterSet):

    nombre = CharFilter(field_name='nombre', label= 'Nombre', lookup_expr='icontains')

    class Meta:
        model = Cliente
        fields =  ['ruc']#('__all__')
        #exclude = ['nombre', 'created', 'modified', 'rentabilidad_presupuesto', 'descripcion', 'monto']