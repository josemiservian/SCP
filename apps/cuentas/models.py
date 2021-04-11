from django.db import models
from django.auth import User

# Create your models here.
class Empleado(models.Model):
    '''Modelo de Empleado de una consultora'''
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    cedula = models.CharField(max_length=15, null=False, blank=False, unique=True)
    nombre = models.CharField(max_length=20, null=False)
    apellido = models.CharField(max_length=20, null=False)
    direccion = models.CharField(max_length=80, null=False)
    fecha_nacimiento = models.DateField(null=False)
    cargo = models.CharField(max_length=20, null=False, default='')
    tarifa = models.FloatField(null=False, default=0)
    estado = models.CharField(max_length=20, null=False, default='Activo')
    #area = models.ForeignKey('areas.Area', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.usuario.username