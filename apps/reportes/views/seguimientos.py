# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Decoradores
from scp.decorators import allowed_users

#Models
from apps.reportes.models import Seguimiento

#Formularios
from apps.reportes.forms import SeguimientoForm, FormCrearSeguimiento


# Create your views here.

class CrearSeguimiento(FormView):
    """ Vista de creacion de Seguimientos"""

    template_name = 'seguimientos/crear.html'
    form_class = FormCrearSeguimiento
    success_url = reverse_lazy('reportes:seguimientos-inicio')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='empleados/login')
@allowed_users(action='add_seguimiento')
def crear_seguimiento(request):

	form = FormCrearSeguimiento

	if request.method == 'POST':
		form = FormCrearseguimiento(request.POST)
		if form.is_valid():
			form.save()
			return redirect('reportes:seguimientos-listar')

	context = {'form':form}
	return render(request, 'seguimientos/crear.html', context)

@login_required(login_url='empleados/login')
@allowed_users(action='view_seguimiento')
def listar_seguimientos(request):

    seguimientos = Seguimiento.objects.all()
    return render(request, 'seguimientos/listar.html', {'seguimientos':seguimientos})

@login_required(login_url='empleados/login')
@allowed_users(action='update_seguimiento')
def actualizar_seguimiento(request, pk):

	seguimiento = Seguimiento.objects.get(id=pk)
	form = SeguimientoForm(instance=seguimiento)

	if request.method == 'POST':
		form = SeguimientoForm(request.POST, instance=seguimiento)
		if form.is_valid():
			form.save()
			return redirect('reportes:seguimientos-listar')

	context = {'form':form}
	return render(request, 'seguimientos/modificar.html', context)


@login_required(login_url='empleados/login')
@allowed_users(action='delete_seguimiento')
def borrar_seguimiento(request, pk):
	
    seguimiento = Seguimiento.objects.get(id=pk)
    if request.method == "POST":
        seguimiento.delete()
        return redirect('reportes:seguimientos-listar')
        
    context = {'seguimiento':seguimiento}
    return render(request, 'seguimientos/borrar.html', context)
