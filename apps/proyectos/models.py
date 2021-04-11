from django.db import models
import datetime as dt

class Cliente(models.Model):
    '''Clientes de la consultora'''

    nombre = models.CharField(max_length=60, null=False, blank=False)
    rubro = models.CharField(max_length=30, null=False, blank=False)
    estado = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.nombre


class Contrato(models.Model):
    '''Contratos establecidos con la consultora.
    Las rentabilidades se estiman de la siguiente manera:
        -Malo/Deficiente: <1
        -Normal/Estimado = 1
        -Excelente >1'''

    cliente = models.ForeignKey('proyectos.Cliente', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, null=False)
    descripcion = models.CharField(max_length=80, null=False)
    monto = models.IntegerField(null=False)
    horas_presupuestadas = models.IntegerField(default=0)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_servicio = models.ForeignKey('gestion.Servicio', on_delete=models.CASCADE)
    horas_ejecutadas = models.IntegerField(null=True, default=0)
    gastos = models.IntegerField(default=0)
    rentabilidad_horas = models.FloatField(null=True, default=1) 
    rentabilidad_presupuesto = models.FloatField(null=True, default=1)
    estado = models.CharField(max_length=15, null=False, default='Activo')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def sumar_horas(self, cantidad_horas):
        '''Aumenta la cantidad de horas ejecutadas en base a los cargado
        por los analistas.'''

        self.horas_ejecutadas = self.horas_ejecutadas + cantidad_horas
        if self.horas_ejecutadas < 0:
            self.horas_ejecutadas = 0

    def sumar_gastos(self, monto_gastado):
        '''Suma los diferentes gastos asociados al contrato.'''
        self.gastos = self.gastos + monto_gastado
        if self.gastos < 0:
            self.gastos = 0

    def calcular_rentabilidad_horas(self):
        '''Calculo de la rentabilidad del proyecto basado en horas.
        Fórmula: horas_presupuestadas / horas_ejecutadas.'''
        if self.horas_ejecutadas <= 0:
            self.rentabilidad_horas = 1
        else:
            self.rentabilidad_horas = self.horas_presupuestadas / self.horas_ejecutadas

    def calcular_rentabilidad_presupuesto(self):
        '''Calculo de la rentabilidad del proyecto basado en el presupuesto.
        Fórmula: monto / gastos.'''
        if self.gastos <= 0:
            self.rentabilidad_presupuesto = 1
        else:
            self.rentabilidad_presupuesto = self.monto / self.gastos

    def maestro_calculos(self, horas, gastos):
        '''Método maestro para calcular horas, gastos y rentabilidad'''
        self.sumar_horas(horas)
        self.sumar_gastos(gastos)
        self.calcular_rentabilidad_horas()
        self.calcular_rentabilidad_presupuesto()

    def __str__(self):
        """Retorna nombre de Proyecto."""
        return self.nombre
    



class EquipoProyecto(models.Model):
    '''Equipos conformados para la realización de proyectos'''

    nombre = models.CharField(max_length=40, blank=True, null=True)
    descripcion = models.CharField(max_length=80, blank=True, null=True)
    contrato = models.ForeignKey('proyectos.Contrato', on_delete=models.CASCADE)
    lider_proyecto = models.ForeignKey('gestion.Empleado', on_delete=models.CASCADE)
    #rol = models.ForeignKey('roles.Rol', on_delete=models.CASCADE)
    #tarifa_asignada = models.FloatField(null=False)

    def __str__(self):
        return self.nombre


class MiembroEquipoProyecto(models.Model):
    '''Empleados relacionados a cada equipo.'''
    
    equipo_proyecto = models.ForeignKey('proyectos.EquipoProyecto', on_delete=models.CASCADE)
    empleado = models.ForeignKey('gestion.Empleado', on_delete=models.CASCADE)
    #rol = models.ForeignKey('gestion.Rol', on_delete=models.CASCADE)
    LIDER_PROYECTO = 'LPR'
    CONSULTOR = 'CON'
    AUDITOR = 'AUD'

    ROLES_CHOICES = [
        (LIDER_PROYECTO, 'Lider del Proyecto'),
        (CONSULTOR, 'Consultor'),
        (AUDITOR, 'Auditor'),
    ]
    rol = models.CharField(
        max_length=3, 
        choices=ROLES_CHOICES, 
        default=CONSULTOR)
    tarifa_asignada = models.FloatField(null=False)

    def __str__(self):
        return self.empleado.nombre + ' ' + self.empleado.apellido + ' - ' + self.rol


class RegistroHora(models.Model):
    '''Registro de horas de las tareas de los proyectos en los cuales se 
    encuentran los empleados de la consultora.'''

    empleado = models.ForeignKey('gestion.Empleado', on_delete=models.CASCADE)
    contrato = models.ForeignKey('proyectos.Contrato', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60, null=False)
    detalle = models.CharField(max_length=250, null=False)
    fecha = models.DateField(null=False)
    hora_inicio =  models.TimeField(default=dt.time(00, 00), null=False)
    hora_fin =  models.TimeField(default=dt.time(00, 00), null=False)

    def __str__(self):
        return self.nombre