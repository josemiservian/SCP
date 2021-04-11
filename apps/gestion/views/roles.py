# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Decoradores
from scp.decorators import allowed_users

#Models
from apps.gestion.models import Rol

#Formularios
from apps.gestion.forms import RolForm, FormCrearRol

# Create your views here.

class CrearRol(FormView):
    """ Vista de creacion de Roles"""

    template_name = 'roles/crear.html'
    form_class = FormCrearRol
    success_url = reverse_lazy('gestion:roles-listar')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='empleados/login')
@allowed_users(action='add_rol')
def crear_roles(request):

	form = FormCrearRol

	if request.method == 'POST':
		form = FormCrearRol(request.POST)
		if form.is_valid():
			form.save()
			return redirect('gestion:roles-listar')

	context = {'form':form}
	return render(request, 'roles/crear.html', context)

@login_required(login_url='empleados/login')
@allowed_users(action='view_rol')
def listar_roles(request):

    roles = Rol.objects.all()
    return render(request, 'roles/listar.html', {'roles':roles})

@login_required(login_url='empleados/login')
@allowed_users(action='change_rol')
def actualizar_rol(request, pk):

	rol = Rol.objects.get(id=pk)
	form = RolForm(instance=rol)

	if request.method == 'POST':
		form = RolForm(request.POST, instance=rol)
		if form.is_valid():
			form.save()
			return redirect('gestion:roles-listar')

	context = {'form':form}
	return render(request, 'roles/modificar.html', context)


@login_required(login_url='empleados/login')
@allowed_users(action='delete_rol')
def borrar_rol(request, pk):
	
    rol = Rol.objects.get(id=pk)
    if request.method == "POST":
        rol.delete()
        return redirect('gestion:roles-listar')
        
    context = {'rol':rol}
    return render(request, 'roles/borrar.html', context)
