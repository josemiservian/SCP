from django.db import models
from django.contrib.auth.models import User

#Modelos
class Area(models.Model):
    '''Modelo de Areas de una consultora '''
    nombre = models.CharField(max_length=20, null=False)
    #id_gerente = models.ForeignKey('empleados.Empleado', on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, null=False)
    
    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    '''Modelo de Empleado de una consultora'''
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    cedula = models.CharField(max_length=15, null=False, blank=False, unique=True)
    nombre = models.CharField(max_length=20, null=False)
    apellido = models.CharField(max_length=20, null=False)
    direccion = models.CharField(max_length=80, null=False)
    fecha_nacimiento = models.DateField(null=False)
    cargo = models.ForeignKey('gestion.Cargo', on_delete=models.CASCADE, null=True)
    tarifa = models.FloatField(null=False, default=0)
    estado = models.CharField(max_length=20, null=False, default='Activo')
    #area = models.ForeignKey('areas.Area', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.usuario.username


class Rol(models.Model):
    '''Modelo de roles que tendran los empleados a la hora de trabajar en un 
    determinado proyecto. A cada empleado se le será asignado un rol para que
    tendrá que cumplir en la realizació del proyecto.'''

    nombre = models.CharField(max_length=20, null=False)
    tipo = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    '''Modelo de servicios que una consultora puede ofrecer a sus clientes.'''
    
    detalle =  models.CharField(max_length=30, null=False)
    descripcion = models.CharField(max_length=60, null=False)
    estado_final = models.CharField(max_length=15, null=False)
    costo = models.FloatField(null=False)
    area = models.ForeignKey('gestion.Area', on_delete=models.CASCADE)

    def __str__(self):
        return self.detalle


class Cargo(models.Model):
    '''Modelo de los cargos posibles para un empleado de la consultora
    y sus tarifas (por hora)'''
    cargo = models.CharField(max_length=30, null=False)
    tarifa_gs = models.FloatField(null=False)
    tarifa_ds = models.FloatField(null=False)

    def __str__(self):
        return self.cargo