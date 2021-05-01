#Django
import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter

#Modelos
from apps.gestion.models import Servicio

class ServicioFilter(django_filters.FilterSet):

    nombre = CharFilter(field_name='detalle', label= 'Detalle', lookup_expr='icontains')

    class Meta:
        model = Servicio
        fields =  ['estado_final', 'area']
        
