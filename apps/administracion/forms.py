# Django
from django import forms

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
    fecha = forms.DateField(widget=forms.SelectDateWidget)
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


class GastoForm(forms.ModelForm):
    class Meta: 
        model = Gasto
        fields = ('motivo', 'detalle', 'fecha', 'gasto', 'empleado', 'contrato')

#Facturaciones
class FormCrearFacturacion(forms.Form):
    
    detalle = forms.CharField(min_length=3, max_length=30)
    descripcion = forms.CharField(min_length=3, max_length=60)
    forma_pago = forms.CharField(min_length=3, max_length=15)
    fecha_emision = forms.DateField(widget=forms.SelectDateWidget)
    fecha_vencimiento = forms.DateField(widget=forms.SelectDateWidget)
    monto_total = forms.FloatField()
    monto_facturacion = forms.FloatField()
    saldo_facturacion = forms.FloatField()
    estado = forms.CharField(min_length=3, max_length=15)

    def save(self):
        """Crea y guarda una factura"""
        data = self.cleaned_data
        factura = Facturacion(detalle=data['detalle'], descripcion=data['descripcion'],
                              forma_pago=data['forma_pago'], fecha_emision=data['fecha_emision'],
                              fecha_vencimiento=data['fecha_vencimiento'], 
                              monto_total=data['monto_total'],
                              monto_facturacion=data['monto_facturacion'], 
                              saldo_facturacion=data['saldo_facturacion'],
                              estado=data['estado'])
        factura.save()


class FacturaForm(forms.ModelForm):
    class Meta: 
        model = Facturacion
        fields = ('detalle','descripcion','forma_pago','fecha_emision',
                  'fecha_vencimiento','monto_total','monto_facturacion',
                  'saldo_facturacion','estado')


#Pagos
class FormCrearPago(forms.Form):
    
    detalle = forms.CharField(min_length=3, max_length=30)
    descripcion = forms.CharField(min_length=3, max_length=60)
    monto = forms.FloatField()
    nro_cuota = forms.IntegerField()
    fecha = forms.DateField(widget=forms.SelectDateWidget)
    saldo = forms.FloatField()
    estado = forms.ChoiceField(
        choices=(('P', 'Pagado'), ('NP', 'No pagado')))

    def save(self):
        """Crea y guarda un pago"""
        data = self.cleaned_data
        pago = Pago(detalle=data['detalle'], descripcion=data['descripcion'],
                    monto=data['monto'], nro_cuota=data['nro_cuota'],
                    fecha=data['fecha'], saldo=data['saldo'], estado=data['estado'],)
        pago.save()


class PagoForm(forms.ModelForm):
    class Meta: 
        model = Pago
        fields = ('detalle','descripcion','monto','nro_cuota',
                  'fecha','saldo','estado')