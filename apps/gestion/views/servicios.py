# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Decoradores
from scp.decorators import allowed_users

#Models
from apps.gestion.models import Servicio

#Formularios
from apps.gestion.forms import ServicioForm, FormCrearServicio

# Create your views here.

class CrearServicio(FormView):
    """ Vista de creacion de Servicios"""

    template_name = 'servicios/crear.html'
    form_class = FormCrearServicio
    success_url = reverse_lazy('gestion:servicios-inicio')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='empleados/login')
@allowed_users(action='add_servicio')
def crear_servicio(request):

	form = FormCrearServicio

	if request.method == 'POST':
		form = FormCrearServicio(request.POST)
		if form.is_valid():
			form.save()
			return redirect('gestion:servicios-listar')

	context = {'form':form}
	return render(request, 'servicios/crear.html', context)

@login_required(login_url='empleados/login')
@allowed_users(action='view_servicio')
def listar_servicios(request):

    servicios = Servicio.objects.all()
    return render(request, 'servicios/listar.html', {'servicios':servicios})

@login_required(login_url='empleados/login')
@allowed_users(action='change_servicio')
def actualizar_servicio(request, pk):

	servicio = Servicio.objects.get(id=pk)
	form = ServicioForm(instance=servicio)

	if request.method == 'POST':
		form = ServicioForm(request.POST, instance=servicio)
		if form.is_valid():
			form.save()
			return redirect('gestion:servicios-listar')

	context = {'form':form}
	return render(request, 'servicios/modificar.html', context)


@login_required(login_url='empleados/login')
@allowed_users(action='delete_servicio')
def borrar_servicio(request, pk):
	
    servicio = Servicio.objects.get(id=pk)
    if request.method == "POST":
        servicio.delete()
        return redirect('gestion:servicios-listar')
        
    context = {'servicio':servicio}
    return render(request, 'servicios/borrar.html', context)
