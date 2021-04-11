# Django
from django import forms

# Models
from apps.proyectos.models import Cliente, Contrato, EquipoProyecto, MiembroEquipoProyecto, RegistroHora
from apps.gestion.models import Empleado, Rol, Servicio
import datetime as dt

#Constantes
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)] #Para desplegar una lista de horas


#Formularios para Clientes
class FormCrearCliente(forms.Form):
    
    nombre = forms.CharField(min_length=3, max_length=30)
    rubro = forms.CharField(min_length=4, max_length=50)
    estado = forms.CharField(max_length=15)

    def save(self):
        """Crea y guarda un cliente"""
        data = self.cleaned_data
        cliente = Cliente(nombre=data['nombre'], rubro=data['rubro'],estado=data['estado'],)
        cliente.save()


class ClienteForm(forms.ModelForm):
    """Formulario de Cliente."""

    class Meta:
        
        model = Cliente
        fields = ('nombre', 'rubro','estado')


#Formularios para Contratos
class FormCrearContrato(forms.Form):
    
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())
    nombre = forms.CharField(min_length=4, max_length=30)
    descripcion = forms.CharField(max_length=80)
    monto = forms.CharField(max_length=8)
    horas_presupuestadas = forms.IntegerField()
    fecha_inicio = forms.DateField(widget=forms.SelectDateWidget)
    fecha_fin = forms.DateField(widget=forms.SelectDateWidget)
    tipo_servicio = forms.ModelChoiceField(queryset=Servicio.objects.all())
    #estado = forms.CharField(max_length=15)
    #rentabilidad = forms.IntegerField()
    #horas_ejecutadas = forms.IntegerField()

    def save(self):
        """Crea y guarda el contrato"""
        data = self.cleaned_data
        contrato = Contrato(cliente=data['cliente'],nombre=data['nombre'],
                            descripcion=data['descripcion'],monto=data['monto'],
                            horas_presupuestadas=data['horas_presupuestadas'],
                            fecha_inicio=data['fecha_inicio'],
                            fecha_fin=data['fecha_fin'],tipo_servicio=data['tipo_servicio'])#,
                            #estado=data['estado'],rentabilidad=data['rentabilidad'],
                            #horas_ejecutadas=data['horas_ejecutadas'])
        contrato.save()


class ContratoForm(forms.ModelForm):
    class Meta:
        
        model = Contrato
        fields = ('cliente','nombre','descripcion','monto','horas_presupuestadas',
                  'fecha_inicio','fecha_fin','tipo_servicio')#,'estado','rentabilidad',
                  #'horas_ejecutadas')


#Formularios para Registro de horas
class FormCrearRegistroHora(forms.Form):
    
    contrato = forms.ModelChoiceField(queryset=Contrato.objects.all())
    nombre = forms.CharField(min_length=3, max_length=30)
    detalle = forms.CharField(min_length=3, max_length=50)
    fecha = forms.DateField(widget=forms.SelectDateWidget)
    hora_inicio = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))#widget=forms.SelectDateWidget
    hora_fin = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))

    def save(self, request):
        """Crea y guarda un registro"""
        data = self.cleaned_data
        empleado = Empleado.objects.filter(usuario__username=request.user)[0]
        registro = RegistroHora(empleado=empleado, contrato=data['contrato'],
                                nombre=data['nombre'], detalle=data['detalle'],
                                fecha=data['fecha'], hora_inicio=data['hora_inicio'],
                                hora_fin=data['hora_fin'],)
        registro.save()


class RegistroForm(forms.ModelForm):
    class Meta: 
        model = RegistroHora
        fields = ('contrato', 'nombre','detalle','fecha','hora_inicio','hora_fin')


#Formularios de Equipos de Proyecto
class FormCrearEquipo(forms.Form):
    
    nombre = forms.CharField(min_length=3, max_length=30)
    descripcion = forms.CharField(min_length=3, max_length=80)
    contrato = forms.ModelChoiceField(queryset=Contrato.objects.all())
    lider = forms.ModelChoiceField(queryset=Empleado.objects.all())
    

    def save(self):
        """Crea y guarda un cliente"""
        data = self.cleaned_data
        equipo = EquipoProyecto(nombre=data['nombre'], descripcion=data['descripcion'],
                                contrato=data['contrato'], lider_proyecto=data['lider'])
        equipo.save()


class FormAddMiembro(forms.Form):
    
    #equipo = forms.ModelChoiceField(queryset=EquipoProyecto.objects.all())
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.all())
    rol = forms.ChoiceField(choices=(
        ('CON','Consultor'),
        ('LPR','Lider del Proyecto'),
        ('AUD','Auditor'))
    )
    #tarifa_asignada = forms.FloatField()
    

    def save(self, equipo_id, usuario):
        """Añade a un empleado a un equipo de Proyecto"""
        data = self.cleaned_data
        empleado = Empleado.objects.filter(usuario__username=usuario)[0]
        #cargo = Cargo.objects.filter(empleado__usuario__username=usuario)[0]
        miembro_equipo = MiembroEquipoProyecto(
            equipo_proyecto_id=equipo_id,  
            empleado=data['empleado'], 
            rol=data['rol'],
            tarifa_asignada=empleado.tarifa#cargo.tarifa
        )
        miembro_equipo.save()


class EquipoForm(forms.ModelForm):
    class Meta:
        
        model = EquipoProyecto
        fields = ('nombre','descripcion','contrato','lider_proyecto')
    

class MiembroForm(forms.ModelForm):
    class Meta:
        
        model = MiembroEquipoProyecto
        fields = ('empleado','rol')#'equipo_proyecto',,'tarifa_asignada'

