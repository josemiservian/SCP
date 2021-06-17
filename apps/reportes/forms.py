# Django
from django import forms
from django.forms import*

# Models
from apps.cuentas.models import Empleado
from apps.proyectos.models import Contrato, RegistroHora
from apps.reportes.models import Seguimiento


class FormCrearSeguimiento(Form):
    
    detalle = CharField(max_length=30)
    descripcion = CharField(max_length=50)
    estado_inicial = CharField(max_length=15)
    estado_final = CharField(max_length=15)
    cant_horas_invertidas = IntegerField()
    contrato = ModelChoiceField(Contrato.objects.all())
    empleado = ModelChoiceField(Empleado.objects.all())
    registro = ModelChoiceField(RegistroHora.objects.all())
    
    def save(self):
        """Crea y guarda un cliente"""
        data = self.cleaned_data
        seguimiento = Seguimiento(detalle=data['detalle'], descripcion=data['descripcion'],
                                  estado_inicial=data['estado_inicial'], 
                                  estado_final=data['estado_final'],
                                  cant_horas_invertidas=data['cant_horas_invertidas'], 
                                  contrato=data['contrato'], empleado=data['empleado'],
                                  registro=data['registro'],
                                  )
        seguimiento.save()


class SeguimientoForm(ModelForm):
    class Meta: 
        model = Seguimiento
        fields = (
            'detalle','descripcion','estado_inicial','estado_final',
            'cant_horas_invertidas','contrato','empleado'#,'registro'
        )

#REPORTES
class ReportForm(Form):
    date_range = CharField(widget=TextInput(attrs={
       'class': 'form-control',
       'autocomplete': 'off' 
    }))

    