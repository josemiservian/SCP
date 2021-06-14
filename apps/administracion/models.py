#Django
from apps.proyectos.models import Propuesta
from datetime import datetime
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from scp.choices import FACTURA_CHOICES, PAGOS_CHOICES

#Modelos



class Facturacion(models.Model):
    '''Modelo para generacion de facturas.'''
    nro_factura = models.CharField(null=False, max_length=15, default='001-001-1234567')
    nro_timbrado = models.IntegerField(null=False, default=123456789)
    vigencia_desde =  models.DateField(null=False, default=timezone.now)
    vigencia_hasta =  models.DateField(null=False, default=timezone.now)
    nombre_cliente = models.CharField(null=False, max_length=100)
    ruc = models.CharField(max_length=15, null=False, default='111111-1')
    forma_pago = models.CharField(max_length=15, null=False, choices=PAGOS_CHOICES)
    fecha_emision = models.DateField(null=False, default=timezone.now)
    fecha_vencimiento = models.DateField(null=False, default=timezone.now)
    monto_facturacion = models.FloatField(null=False, default=11111)
    descripcion = models.CharField(max_length=60, blank=True, null=False, default='')
    estado = models.CharField(max_length=20, choices=PAGOS_CHOICES, default='PENDIENTE DE PAGO')
    plan_facturacion = models.ForeignKey('administracion.PlanFacturacion', on_delete=CASCADE)

    def __str__(self):
        return f'{self.nro_factura}'
    
    def registrar_pago(self):
        '''Registra la factura como pagada'''
        self.estado = 'PAGADO'


class PlanFacturacion(models.Model):

    descripcion = models.CharField(max_length=60, null=False)
    fecha_emision = models.DateField(null=False)
    fecha_vencimiento = models.DateField(null=False)
    monto_facturar = models.FloatField(null=False)
    estado = models.CharField(max_length=25, choices=FACTURA_CHOICES, default='PENDIENTE FACTURACION')
    condicion_pago = models.ForeignKey('proyectos.CondicionPago', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Plan de Facturaciones'

    def __str__(self):
        return self.descripcion

    def emitir_factura(self):
        self.estado = 'FACTURADO'

    def emitir_pago(self):
        self.estado = 'PAGADO'


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
    fecha = models.DateField(null=True, default=None)
    gasto = models.FloatField(null=False, default=0)
    empleado = models.ForeignKey('cuentas.Empleado', on_delete=models.CASCADE, null=True, default=None)
    contrato = models.ForeignKey('proyectos.Contrato', on_delete=models.CASCADE, null=True, default=None)
    propuesta = models.ForeignKey('proyectos.Propuesta', related_name='gasto_propuesta', on_delete=models.CASCADE, null=True)
    registro = models.ForeignKey(
        'proyectos.RegistroHora', 
        null=True,
        default=None, 
        on_delete=models.CASCADE)

    def __str__(self):
        if self.propuesta is None:
            return self.motivo + ' - ' + self.empleado.nombre + ' ' + self.empleado.apellido + ' - ' + self.contrato.nombre
        else:
            return f'{self.propuesta} - {self.motivo}'
    
    def cargar_gasto(self, gasto):
        self.gasto = self.gasto + gasto


class Pago(models.Model):
    '''Modelo para generacion de Pagos a la consultora.'''
    
    contrato = models.ForeignKey('proyectos.Contrato', on_delete=models.CASCADE)
    factura = models.ForeignKey('administracion.Facturacion', on_delete=models.CASCADE)
    detalle = models.CharField(max_length=50, blank=True, null=False)
    descripcion = models.CharField(max_length=60, blank=True, null=False, default='') 
    monto = models.FloatField(null=False)
    #nro_cuota = models.IntegerField()
    fecha = models.DateField(null=False)
    #saldo = models.FloatField(null=False)
    ESTADOS_CHOICES = (
        ('P', 'Pagado'),
        ('NP', 'No pagado')
    )
    estado = models.CharField(max_length=10, choices=ESTADOS_CHOICES)

    def __str__(self):
        return self.detalle

