# Django
from apps.proyectos.models import CondicionPago, Contrato
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View
from django.template.loader import get_template
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from xhtml2pdf import pisa

#Python
from dateutil import relativedelta
import io

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
            nombre = plan.contrato.cliente.nombre,
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


@login_required(login_url='cuentas:login')
@allowed_users(action='view_planfacturacion')
def listar_planes_facturacion(request):
    '''Lista los planes de facturacion'''
    
    planes_facturacion = PlanFacturacion.objects.all()
    context = {'planes_facturacion':planes_facturacion}
    return render(request, 'planesFacturacion/listar.html', context)

def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


class FacturaPdf(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('facturaciones/factura.html')
            context = {
                'factura':Facturacion.objects.get(id=self.kwargs['pk'])
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(html, dest=response)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('administracion:facturaciones-listar'))