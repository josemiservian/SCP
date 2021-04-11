# Django
from django import forms

# Models
from apps.gestion.models import Empleado
from apps.proyectos.models import Contrato, RegistroHora
from apps.reportes.models import Seguimiento


class FormCrearSeguimiento(forms.Form):
    
    detalle = forms.CharField(max_length=30)
    descripcion = forms.CharField(max_length=50)
    estado_inicial = forms.CharField(max_length=15)
    estado_final = forms.CharField(max_length=15)
    cant_horas_invertidas = forms.IntegerField()
    contrato = forms.ModelChoiceField(Contrato.objects.all())
    empleado = forms.ModelChoiceField(Empleado.objects.all())
    registro = forms.ModelChoiceField(RegistroHora.objects.all())
    
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


class SeguimientoForm(forms.ModelForm):
    class Meta: 
        model = Seguimiento
        fields = (
            'detalle','descripcion','estado_inicial','estado_final',
            'cant_horas_invertidas','contrato','empleado','registro'
        )