from django.test import TestCase
from apps.administracion.models import *
from apps.proyectos.models import *

# Create your tests here.

#Preguntar si poner como gasto eliminado o algo así y poner el valor en negativo
#o poner para realizar todo el proceso de matchear fechas, detalles
registro = RegistroHora.objects.filter(id=54)[0]
gasto = Gasto.objects.filter(detalle=registro.detalle, fecha=registro.fecha)