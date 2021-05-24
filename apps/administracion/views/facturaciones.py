# Django
from apps.proyectos.models import CondicionPago, Contrato
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Python
from dateutil import relativedelta

#Decoradores
from scp.decorators import allowed_users

#Models
from apps.administracion.models import Facturacion, PlanFacturacion

#Formularios
from apps.administracion.forms import FacturaForm, FormCrearFacturacion


# Create your views here.
class CrearFactura(FormView):
    """ Vista de creacion de Facturas"""

    template_name = 'facturaciones/crear.html'
    form_class = FormCrearFacturacion
    success_url = reverse_lazy('administracion:facturaciones-listar')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='cuentas:login')
@allowed_users(action='add_facturacion')
def crear_factura(request):

	form = FormCrearFacturacion()

	if request.method == 'POST':
		form = FormCrearFacturacion(request.POST)
		if form.is_valid():
			form.save()
			return redirect('administracion:facturaciones-listar')

	context = {'form':form}
	return render(request, 'facturaciones/crear.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_facturacion')
def listar_facturas(request):

    facturas = Facturacion.objects.all()
    return render(request, 'facturaciones/listar.html', {'facturas':facturas})

@login_required(login_url='cuentas:login')
@allowed_users(action='change_facturacion')
def actualizar_factura(request, pk):

	factura = Facturacion.objects.get(id=pk)
	form = FacturaForm(instance=factura)

	if request.method == 'POST':
		form = FacturaForm(request.POST, instance=factura)
		if form.is_valid():
			form.save()
			return redirect('administracion:facturaciones-listar')

	context = {'form':form}
	return render(request, 'facturaciones/modificar.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='delete_facturacion')
def borrar_factura(request, pk):
	
    factura = Facturacion.objects.get(id=pk)
    if request.method == "POST":
        factura.delete()
        return redirect('administracion:facturaciones-listar')
        
    context = {'factura':factura}
    return render(request, 'facturaciones/borrar.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='change_planfacturacion')
def emitir_factura(request, pk):
        
    plan = PlanFacturacion.objects.get(id=pk)
    condicion = CondicionPago.objects.get(contrato=plan.contrato)

    if request.method == 'POST':
        plan.emitir_factura()
        factura = Facturacion(
            nro_factura = '001-001-1234567',
            nro_timbrado = 123456789,
            vigencia_desde = plan.fecha_emision, 
            vigencia_hasta = plan.fecha_emision + relativedelta.relativedelta(months=12),
            ruc = plan.contrato.cliente.ruc,
            forma_pago = condicion.forma_pago,
            fecha_emision = plan.fecha_emision,
            fecha_vencimiento = plan.fecha_vencimiento,
            monto_facturacion = plan.monto_facturar,
            descripcion = plan.descripcion,
            estado = 'PENDIENTE DE PAGO',
            plan_facturacion = plan
        )
        plan.save()
        factura.save()

        return redirect('proyectos:condicionPagos-listar', plan.contrato.id)
    
    context = {'plan':plan}
    return render(request, 'facturaciones/emitir_factura.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='view_facturacion')
def detalle_factura(request, pk):

    factura = Facturacion.objects.get(plan_facturacion__id=pk)
    context = {'factura':factura, 'condicion_pago':factura.plan_facturacion.condicion_pago}
    return render(request, 'facturaciones/detalle.html', context)