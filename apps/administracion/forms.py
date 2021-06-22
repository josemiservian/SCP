# Django
from django import forms
from django.forms import widgets

# Models
from apps.administracion.models import Facturacion, Gasto, Pago
from apps.cuentas.models import Empleado
from apps.proyectos.models import Contrato

#Facturaciones
class FormCrearGasto(forms.Form):

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
    motivo = forms.ChoiceField(choices=MOTIVOS_CHOICES)
    detalle = forms.CharField()
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gasto = forms.FloatField()
    empleado = forms.ModelChoiceField(queryset=Empleado.objects.all())
    contrato = forms.ModelChoiceField(queryset=Contrato.objects.all())
    #registro = forms.

    def save(self):
        """Crea y guarda un gasto"""
        data = self.cleaned_data
        gasto = Gasto(motivo=data['motivo'], detalle=data['detalle'], 
                        fecha=data['fecha'], gasto=data['gasto'], 
                        empleado=data['empleado'], contrato=data['contrato'])
        gasto.save()
        return gasto


class GastoForm(forms.ModelForm):
    class Meta: 
        model = Gasto
        fields = ('motivo', 'detalle', 'fecha', 'gasto', 'empleado', 'contrato')
        widgets = {'fecha': forms.SelectDateWidget(years=range(1900, 2030))}

#Facturaciones
class FormCrearFacturacion(forms.Form):
    
    nro_factura = forms.IntegerField()
    nro_timbrado = forms.IntegerField()
    vigencia_desde = forms.DateField()
    vigencia_hasta = forms.DateField()
    ruc = forms.CharField(min_length=6, max_length=15)
    forma_pago = forms.CharField(min_length=3, max_length=15)
    fecha_emision = forms.DateField(widget=forms.SelectDateWidget)
    fecha_vencimiento = forms.DateField(widget=forms.SelectDateWidget)
    monto_facturacion = forms.FloatField()
    descripcion = forms.CharField(min_length=3, max_length=60)
    estado = forms.CharField(min_length=3, max_length=15)

    def save(self):
        """Crea y guarda una factura"""
        data = self.cleaned_data
        factura = Facturacion(
            data['nro_factura'], data['nro_timbrado'], data['vigencia_desde'],
            data['vigencia_hasta'], data['ruc'], data['forma_pago'],
            data['fecha_emision'], data['fecha_vencimiento'], 
            data['monto_facturacion'], data['descripcion'], data['estado']
        )
        factura.save()


class FacturaForm(forms.ModelForm):
    class Meta: 
        model = Facturacion
        fields = ('__all__')
        widgets = {
            'vigencia_desde': forms.SelectDateWidget(years=range(1900, 2030)),
            'vigencia_hasta': forms.SelectDateWidget(years=range(1900, 2030)),
            'fecha_emision': forms.SelectDateWidget(years=range(1900, 2030)),
            'fecha_vencimiento': forms.SelectDateWidget(years=range(1900, 2030))
        }

#Pagos
class FormCrearPago(forms.Form):
    
    detalle = forms.CharField(min_length=3, max_length=30)
    descripcion = forms.CharField(min_length=3, max_length=60)
    monto = forms.FloatField()
    #nro_cuota = forms.IntegerField()
    fecha = forms.DateField(widget=forms.SelectDateWidget)
    #saldo = forms.FloatField()
    estado = forms.ChoiceField(
        choices=(('P', 'Pagado'), ('NP', 'No pagado')))

    def save(self):
        """Crea y guarda un pago"""
        data = self.cleaned_data
        pago = Pago(detalle=data['detalle'], descripcion=data['descripcion'],
                    monto=data['monto'], 
                    fecha=data['fecha'], estado=data['estado'],)
        pago.save()


class PagoForm(forms.ModelForm):
    class Meta: 
        model = Pago
        fields = ('detalle','descripcion','monto',
                  'fecha','estado')