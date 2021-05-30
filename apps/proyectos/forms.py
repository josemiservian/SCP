# Django
from django import forms
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT
from django.forms import formset_factory
from django.contrib.admin import site as admin_site, widgets
from django.db.models import ManyToOneRel

# Models
from apps.proyectos.models import * #Cliente, Contrato, EquipoProyecto, MiembroEquipoProyecto, RegistroHora, Propuesta, PropuestaDetalle
from apps.cuentas.models import Empleado
from apps.gestion.models import Area, Cargo, Rol, Servicio
import datetime as dt

#Python
from datetime import datetime

#Constantes
from scp.choices import PAGOS_CHOICES
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)] #Para desplegar una lista de horas
HORAS = ['%02d:%s' % (h, m)  for h in (list(range(0,24))) for m in ('00', '30')]
HORAS = tuple([(hora,hora) for hora in HORAS])


#Formularios para Clientes
class FormCrearCliente(forms.Form):
    
    nombre = forms.CharField(min_length=3, max_length=30)
    ruc = forms.CharField(min_length=8)
    direccion = forms.CharField(min_length=6)
    telefono = forms.CharField(min_length=6)
    rubro = forms.CharField(min_length=4, max_length=50)
    estado = forms.CharField(max_length=15)

    def save(self):
        """Crea y guarda un cliente"""
        data = self.cleaned_data
        cliente = Cliente(
            nombre=data['nombre'], 
            ruc=data['ruc'],
            direccion=data['direccion'],
            telefono=data['telefono'],
            rubro=data['rubro'],estado=data['estado'],)
        cliente.save()


class ClienteForm(forms.ModelForm):
    """Formulario de Cliente."""
    
    class Meta:
        
        model = Cliente
        fields = ('__all__')
        

#Formularios para Contratos
class FormCrearContrato(forms.Form):
    
    propuesta = forms.ModelChoiceField(queryset=Propuesta.objects.filter(estado='A'))
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())
    nombre = forms.CharField(min_length=4, max_length=30)
    descripcion = forms.CharField(max_length=80)
    monto = forms.FloatField(localize=True)
    horas_presupuestadas = forms.IntegerField(min_value=0)
    fecha_inicio = forms.DateField(widget=forms.SelectDateWidget)
    fecha_fin = forms.DateField(widget=forms.SelectDateWidget)
    tipo_servicio = forms.ModelChoiceField(queryset=Servicio.objects.all())


    def save(self):
        """Crea y guarda el contrato"""
        data = self.cleaned_data
        contrato = Contrato(propuesta=data['propuesta'],cliente=data['cliente'],nombre=data['nombre'],
                            descripcion=data['descripcion'],monto=data['monto'],
                            horas_presupuestadas=data['horas_presupuestadas'],
                            fecha_inicio=data['fecha_inicio'],
                            fecha_fin=data['fecha_fin'],tipo_servicio=data['tipo_servicio'])#,
                            #estado=data['estado'],rentabilidad=data['rentabilidad'],
                            #horas_ejecutadas=data['horas_ejecutadas'])
        contrato.save()
        return contrato.id


class ContratoForm(forms.ModelForm):
    class Meta:
        
        model = Contrato
        fields = ('cliente', 'propuesta','nombre', 'descripcion','monto','horas_presupuestadas',
                  'fecha_inicio','fecha_fin','tipo_servicio')


#Formularios para Entregable
class EntregableForm(forms.ModelForm):
    class Meta:
        
        model = Entregable
        fields = ('__all__')


class FormCondicionPago(forms.Form):
    #contrato = forms.ModelChoiceField(queryset=Contrato.objects.all())
    forma_pago = forms.CharField(widget=forms.Select(choices=PAGOS_CHOICES))
    monto_total = forms.FloatField()
    cantidad_pagos = forms.IntegerField(initial=1, min_value=1)
    dias_vencimiento = forms.IntegerField(initial=10)

    def save(self, contrato):
        data = self.cleaned_data
        condicion_pago = CondicionPago(
            contrato=contrato,
            forma_pago=data['forma_pago'],
            monto_total=data['monto_total'],
            cantidad_pagos=data['cantidad_pagos'],
            dias_vencimiento=data['dias_vencimiento']
        )  
        condicion_pago.save()
        return condicion_pago

CondicionPagoFormset = formset_factory(FormCondicionPago, extra=0)


#Formularios para Condiciones de pago
class CondicionPagoForm(forms.ModelForm):
    class Meta:
        
        model = CondicionPago
        fields = ('__all__')


#Formularios para Registro de horas
class FormCrearRegistroHora(forms.Form):
    
    contrato = forms.ModelChoiceField(queryset=Contrato.objects.all())
    entregable = forms.ModelChoiceField(queryset=Entregable.objects.all())
    nombre = forms.CharField(min_length=3, max_length=30)
    detalle = forms.CharField(min_length=3, max_length=50)
    fecha = forms.DateField(widget=forms.SelectDateWidget)
    hora_inicio = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))#widget=forms.SelectDateWidget
    hora_fin = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))
    horas_trabajadas = forms.CharField(min_length=5, max_length=5, help_text='Horas trabajadas (HH:MM)')

    def clean_horas_trabajadas(self):
        '''Valida que la hora sea válida'''
        horas_trabajadas = self.cleaned_data['horas_trabajadas']
        try:
            datetime.strptime(horas_trabajadas, '%H:%M')
            return horas_trabajadas
        except:
            raise forms.ValidationError(f'{horas_trabajadas} no corresponde al formato HH:MM.')

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        return data

    def save(self, request):
        """Crea y guarda un registro"""
        data = self.cleaned_data
        empleado = Empleado.objects.get(usuario__username=request.user)
        registro = RegistroHora(
            empleado=empleado, contrato=data['contrato'], entregable=data['entregable'],
            nombre=data['nombre'], detalle=data['detalle'], fecha=data['fecha'], 
            hora_inicio=data['hora_inicio'], hora_fin=data['hora_fin'], 
            horas_trabajadas=data['horas_trabajadas'])
        registro.save()
        return registro.id


class RegistroForm(forms.ModelForm):
    
    contrato = forms.ModelChoiceField(queryset=Contrato.objects.all())
    entregable = forms.ModelChoiceField(queryset=Entregable.objects.all())
    nombre = forms.CharField(min_length=3, max_length=30)
    detalle = forms.CharField(min_length=3, max_length=50)
    fecha = forms.DateField(widget=forms.SelectDateWidget)
    hora_inicio = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))#widget=forms.SelectDateWidget
    hora_fin = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))

    
    class Meta: 
        model = RegistroHora
        fields = ('contrato', 'entregable','nombre','detalle','fecha','hora_inicio','hora_fin')


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


#Formularios para Propuestas
class FormCrearPropuesta(forms.Form):
    
    area = forms.ModelChoiceField(queryset=Area.objects.all())
    gerente = forms.ModelChoiceField(queryset=Empleado.objects.all())
    nombre = forms.CharField(min_length=4, max_length=60)
    porcentaje_ganancia = forms.DecimalField(max_digits=5, decimal_places=3)

    def save(self):
        """Crea y guarda el contrato"""
        data = self.cleaned_data
        propuesta = Propuesta(
            area=data['area'], 
            gerente=data['gerente'],
            nombre=data['nombre'], 
            porcentaje_ganancia=data['porcentaje_ganancia']
        )
        propuesta.save()

        return propuesta.id


class PropuestaForm(forms.ModelForm):
    
    class Meta:
        
        model = Propuesta
        fields = ('area', 'gerente', 'nombre', 'porcentaje_ganancia')


class PropuestaAsociarCliente(forms.ModelForm):
    
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())

    class Meta:
        
        model = Propuesta
        fields = ('cliente',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].widget = widgets.RelatedFieldWidgetWrapper(
            self.fields['cliente'].widget,
            self.instance._meta.get_field('cliente').remote_field,
            admin_site
        ) 

    #def save(self, pk):
    #    data = self.cleaned_data()
    #    propuesta = Propuesta.objects.get(id=pk)
    #    propuesta.cliente = data['cliente']
    #    propuesta.save()


#formularios para Propuesta Detalle
class FormCrearPropuestaDetalle(forms.Form):
    
    servicio = forms.ModelChoiceField(queryset=Servicio.objects.all())
    descripcion = forms.CharField(max_length=500)
    horas_servicio = forms.IntegerField(initial=0)
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all())
    tarifa = forms.FloatField()
    total = forms.FloatField()
    #porcentaje_ganancia
    ganancia = forms.FloatField()
    total_ventas = forms.FloatField()

    def save(self, propuesta):
        """Crea y guarda el detalle de la propuesta"""
        data = self.cleaned_data
        propuesta_detalle = PropuestaDetalle(
            propuesta=Propuesta.objects.get(id=propuesta), 
            servicio=data['servicio'],
            descripcion=data['descripcion'],
            horas_servicio=data['horas_servicio'],
            cargo=data['cargo'],
            tarifa=data['tarifa'],
            total=data['total']
            )
        propuesta_detalle.save()


class PropuestaDetalleForm(forms.ModelForm):
    
    '''area = forms.ModelChoiceField(queryset=Area.objects.all())
    gerente = forms.ModelChoiceField(queryset=Empleado.objects.all())
    nombre = forms.CharField(min_length=4, max_length=60)
    horas_totales = forms.IntegerField(initial=0)
    total = forms.FloatField(initial=0)
    ganancia_esperada = forms.FloatField(initial=0)
    aceptado = forms.BooleanField(initial=False)
    fecha_aceptacion = forms.DateField(widget=forms.SelectDateWidget)'''
    
    class Meta:
        
        model = PropuestaDetalle
        fields = ('__all__')
