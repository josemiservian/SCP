#Django
from django.db import models
from django.utils import timezone

class Facturacion(models.Model):
    '''Modelo para generacion de facturas.'''
    detalle = models.CharField(max_length=30, blank=True, null=False)
    descripcion = models.CharField(max_length=60, blank=True, null=False, default='')
    forma_pago = models.CharField(max_length=15, null=False)
    fecha_emision = models.DateField(null=False)
    fecha_vencimiento = models.DateField(null=False)
    monto_total = models.FloatField(null=False)
    monto_facturacion = models.FloatField(null=False)
    saldo_facturacion = models.FloatField(null=False)
    estado = models.CharField(max_length=10)

    def __str__(self):
        return self.detalle


class Gasto(models.Model):
    '''Modelo que registra los gastos realizados por los empleados durante
    la realizacion de un proyecto'''
    VIATICOS = 'VIATICOS'
    COMBUSTIBLE = 'COMBUSTIBLE'
    LOGISTICA = 'LOGISTICA'
    HONORARIOS = 'HONORARIOS'
    ALQUILERES = 'ALQUILERES'
    ARANCELES = 'ARANCELES'
    OTROS = 'OTROS'

    MOTIVOS_CHOICES = [
        
        (VIATICOS, 'Viáticos por viajes'),
        (COMBUSTIBLE, 'Reposición de combustible'),
        (LOGISTICA, 'Materiales para logística'),
        (HONORARIOS, 'Honorarios profesionales'),
        (ALQUILERES, 'Alquileres'),
        (ARANCELES, 'Aranceles por plataformas'),
        (OTROS, 'Otros'),
    ]
    motivo = models.CharField(
        max_length=15, 
        choices=MOTIVOS_CHOICES, 
        default=OTROS)
    detalle = models.CharField(max_length=75, blank=True, null=False, default='')
    fecha = models.DateField(null=False, default=timezone.now())
    gasto = models.FloatField(null=False, default=0)
    empleado = models.ForeignKey('gestion.Empleado', null=False, on_delete=models.CASCADE)
    contrato = models.ForeignKey('proyectos.Contrato', null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.motivo + ' - ' + self.empleado.nombre + ' ' + self.empleado.apellido + ' - ' + self.contrato.nombre
    
    def cargar_gasto(self, gasto):
        self.gasto = self.gasto + gasto


class Pago(models.Model):
    '''Modelo para generacion de Pagos a la consultora.'''
    
    detalle = models.CharField(max_length=30, blank=True, null=False)
    descripcion = models.CharField(max_length=60, blank=True, null=False, default='') 
    monto = models.FloatField(null=False)
    nro_cuota = models.IntegerField()
    fecha = models.DateField(null=False)
    saldo = models.FloatField(null=False)
    estado = models.CharField(max_length=10)

    def __str__(self):
        return self.detalle