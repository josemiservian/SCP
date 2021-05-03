#Django
import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter

#Modelos
from apps.cuentas.models import Empleado

class EmpleadoFilter(django_filters.FilterSet):

    nombre = CharFilter(field_name='nombre', label= 'Nombre', lookup_expr='icontains')

    class Meta:
        model = Empleado
        fields =  ['cedula', 'apellido', 'cargo',]#('__all__')
        #exclude = ['nombre', 'created', 'modified', 'rentabilidad_presupuesto', 'descripcion', 'monto']