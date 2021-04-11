# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Decoradores
from scp.decorators import allowed_users

#Models
from apps.administracion.models import Facturacion

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
@login_required(login_url='empleados/login')
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

@login_required(login_url='empleados/login')
@allowed_users(action='view_facturacion')
def listar_facturas(request):

    facturas = Facturacion.objects.all()
    return render(request, 'facturaciones/listar.html', {'facturas':facturas})

@login_required(login_url='empleados/login')
@allowed_users(action='change_facturacion')
def actualizar_factura(request, pk):

	factura = Facturacion.objects.get(id=pk)
	form = FacturaForm(instance=factura)

	if request.method == 'POST':
		form = FacturaForm(request.POST, instance=factura)
		if form.is_valid():
			form.save()
			return redirect('facturaciones:listar')

	context = {'form':form}
	return render(request, 'facturaciones/modificar.html', context)


@login_required(login_url='empleados/login')
@allowed_users(action='delete_facturacion')
def borrar_factura(request, pk):
	
    factura = Facturacion.objects.get(id=pk)
    if request.method == "POST":
        factura.delete()
        return redirect('administracion:facturaciones-listar')
        
    context = {'factura':factura}
    return render(request, 'facturaciones/borrar.html', context)
