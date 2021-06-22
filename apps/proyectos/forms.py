# Django
from django import forms
from django.db.models import fields
from django.forms import formset_factory, BaseInlineFormSet

# Models
from apps.proyectos.models import * #Cliente, Contrato, EquipoProyecto, MiembroEquipoProyecto, RegistroHora, Propuesta, PropuestaDetalle
from apps.cuentas.models import Empleado
from apps.gestion.models import Area, Cargo, Servicio
import datetime as dt

#Python
from datetime import datetime
from scp import widgets

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
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    tipo_servicio = forms.ModelChoiceField(queryset=Servicio.objects.all())

    def clean_propuesta(self):
        '''Valida que ya no se tenga la propuesta seleccionada a otro contrato'''

        propuesta = self.cleaned_data.get('propuesta')
        
        if Contrato.objects.filter(propuesta=propuesta).exists():
            raise forms.ValidationError(f'La propuesta {propuesta} ya se encuentra asociada a otro contrato.') 
        return propuesta

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
        widgets = {
            'fecha_inicio':forms.SelectDateWidget(years=range(1900, 2030)),
            'fecha_fin':forms.SelectDateWidget(years=range(1900, 2030))}


#Formularios para Entregable
class EntregableForm(forms.ModelForm):
    class Meta:
        
        model = Entregable
        fields = ['actividades', 'horas_asignadas', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio':forms.SelectDateWidget(years=range(1900, 2030)),
            'fecha_fin':forms.SelectDateWidget(years=range(1900, 2030))
        }
    
    def clean(self):
        cleaned_data = super(EntregableForm, self).clean()
        print(cleaned_data['horas_asignadas'])


class FormCondicionPago(forms.Form):
    contrato = forms.ModelChoiceField(queryset=Contrato.objects.all(), disabled=True, required=False)
    forma_pago = forms.CharField(widget=forms.Select(choices=PAGOS_CHOICES))
    monto_total = forms.FloatField(widget=forms.NumberInput(attrs={'readonly':'readonly'}))
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
    
    #contrato = forms.ModelChoiceField(queryset=Contrato.objects.all())
    entregable = forms.ModelChoiceField(queryset=Entregable.objects.all())
    nombre = forms.CharField(min_length=3, max_length=30)
    detalle = forms.CharField(min_length=3, max_length=50)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    #hora_inicio = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))#widget=forms.SelectDateWidget
    #hora_fin = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))
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
            empleado=empleado, 
            contrato=Contrato.objects.get(id=data['entregable'].contrato.id), 
            entregable=data['entregable'],
            nombre=data['nombre'], detalle=data['detalle'], fecha=data['fecha'], 
            horas_trabajadas=data['horas_trabajadas'])
        registro.save()
        return registro.id


class RegistroForm(forms.ModelForm):
    
    #contrato = forms.ModelChoiceField(queryset=Contrato.objects.all())
    entregable = forms.ModelChoiceField(queryset=Entregable.objects.all())
    nombre = forms.CharField(min_length=3, max_length=30)
    detalle = forms.CharField(min_length=3, max_length=50)
    fecha = forms.DateField(widget=forms.SelectDateWidget(years=range(2000, 2050)))
    #hora_inicio = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))#widget=forms.SelectDateWidget
    #hora_fin = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))

    
    class Meta: 
        model = RegistroHora
        fields = ('__all__')
        exclude = ['contrato']


#Formularios de Equipos de Proyecto
class FormCrearEquipo(forms.Form):
    
    nombre = forms.CharField(min_length=3, max_length=30)
    descripcion = forms.CharField(min_length=3, max_length=80)
    contrato = forms.ModelChoiceField(queryset=Contrato.objects.all())
    lider = forms.ModelChoiceField(queryset=Empleado.objects.all())
    
    def clean_contrato(self):
        '''Valida que ya no se tenga un equipo asociado a un contrato'''

        contrato = self.cleaned_data.get('contrato')
        
        if EquipoProyecto.objects.filter(contrato=contrato).exists():
            raise forms.ValidationError(f'El contrato "{contrato}" ya se encuentra asociado a un equipo.') 
        return contrato

    def save(self):
        """Crea y guarda un cliente"""
        data = self.cleaned_data
        equipo = EquipoProyecto(
            nombre=data['nombre'], 
            descripcion=data['descripcion'],
            contrato=data['contrato'], 
            lider_proyecto=data['lider']
        )
        equipo.save()


class FormAddMiembro(BaseInlineFormSet):
    
    #equipo = forms.ModelChoiceField(queryset=EquipoProyecto.objects.all())
    #empleado = forms.ModelChoiceField(queryset=Empleado.objects.all())
    #rol = forms.ChoiceField(choices=(
    #    ('CON','Consultor'),
    #    #('LPR','Lider del Proyecto'),
    #    ('AUD','Auditor'))
    #)
    #tarifa_asignada = forms.FloatField()
    
    def clean_empleado(self):
        for form in self.forms:
            form.empleado = self.cleaned_data.get('empleado')
            form.equipo = self.cleaned_data.get('equipo')

            if MiembroEquipoProyecto.objects.filter(empleado=empleado).filter(equipo_proyecto=equipo).exists():
                raise forms.ValidationError(f'El empleado "{empleado}" ya se encuentra asociado al equipo {equipo}.')
            return empleado
            
    '''def save(self, equipo_id, usuario):
        """Añade a un empleado a un equipo de Proyecto"""
        data = self.cleaned_data
        empleado = Empleado.objects.get(usuario__username=usuario)
        #cargo = Cargo.objects.filter(empleado__usuario__username=usuario)[0]
        miembro_equipo = MiembroEquipoProyecto(
            equipo_proyecto_id=equipo_id,  
            empleado=data['empleado'], 
            rol=data['rol'],
            tarifa_asignada=empleado.tarifa#cargo.tarifa
        )
        miembro_equipo.save()'''


class EquipoForm(forms.ModelForm):
    class Meta:
        
        model = EquipoProyecto
        fields = ('__all__')#'nombre','descripcion','contrato','lider_proyecto'
    

class MiembroForm(forms.ModelForm):
    class Meta:
        
        model = MiembroEquipoProyecto
        fields = ('empleado','rol','tarifa_asignada')#'equipo_proyecto',


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

    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['cliente'].widget = widgets.RelatedFieldWidgetWrapper(
    #        self.fields['cliente'].widget,
    #        self.instance._meta.get_field('cliente').remote_field,
    #        admin_site
    #    ) 

    def save(self, pk):
        data = self.cleaned_data
        propuesta = Propuesta.objects.get(id=pk)
        propuesta.cliente = data['cliente']
        propuesta.save()


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

class EntregablesFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        contrato = self.forms[0].cleaned_data['contrato']
        #traer aqui la suma de los entregables YA CREADOS relacionados al proyecto
        total_horas = sum(f.cleaned_data.get('horas_asignadas') for f in self.forms if f.cleaned_data.get('horas_asignadas') is not None)
        if total_horas + contrato.horas_entregables > contrato.horas_presupuestadas:
            raise forms.ValidationError("Las horas asignadas en entregables no debe ser mayor a las horas presupuestadas del contrato")
        else:
            return

class IntegranteFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        integrantes = []
        equipo = self.forms[0].cleaned_data.get('equipo_proyecto')
        for form in self.forms:
            if form.cleaned_data.get('empleado') is not None:
                integrantes.append(form.cleaned_data.get('empleado'))
        validacion = [integrante for integrante in integrantes if equipo.lider_proyecto == integrante or integrante.miembroequipoproyecto_set.get(equipo_proyecto=equipo)]
        if len(set(integrantes)) != len(integrantes) or validacion:
            raise forms.ValidationError('Los empleados solamente pueden estar registrados una vez por equipo.')