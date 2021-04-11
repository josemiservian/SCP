from django.db import models

# Create your models here.
class Seguimiento(models.Model):
    
    detalle = models.CharField(max_length=30, null=False)
    descripcion = models.CharField(null=False, max_length=50)
    estado_inicial = models.CharField(null=False, max_length=15)
    estado_final = models.CharField(null=False, max_length=15)
    cant_horas_invertidas = models.IntegerField(null=False)
    contrato = models.ForeignKey('proyectos.Contrato', on_delete=models.CASCADE)
    empleado = models.ForeignKey('gestion.Empleado', on_delete=models.CASCADE)
    registro = models.ForeignKey('proyectos.RegistroHora', on_delete=models.CASCADE)

    def __str__(self):
        return self.detalle