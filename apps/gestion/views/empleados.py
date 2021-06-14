# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import  authenticate, login, logout #views as
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Count, TimeField
from django.db.models.functions import Cast
#Decoradores
from scp.decorators import allowed_users

# Models
from django.contrib.auth.models import User
from apps.cuentas.models import Empleado
from apps.proyectos.models import Contrato, RegistroHora

# Forms
from apps.cuentas.forms import FormularioRegistro, EmpleadoForm


#FUNCIONES
@login_required(login_url='cuentas:login')
@allowed_users(action='add_empleado')
def crear_empleado(request):

	form = FormularioRegistro()

	if request.method == 'POST':
		form = FormularioRegistro(request.POST)
		if form.is_valid():
			form.save()
			return redirect('gestion:empleados-listar')

	context = {'form':form}
	return render(request, 'empleados/crear.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_empleado')
def listar_empleados(request):

    empleados = Empleado.objects.all().order_by('id')
    return render(request, 'empleados/listar.html', {'empleados':empleados})

@login_required(login_url='cuentas:login')
@allowed_users(action='change_empleado')
def actualizar_empleado(request, pk):

	empleado = Empleado.objects.get(id=pk)
	form = EmpleadoForm(
		
		instance=empleado)
	print(form['fecha_nacimiento'].value())
	if request.method == 'POST':
		form = EmpleadoForm(request.POST, instance=empleado)
		if form.is_valid():
			form.save()
			return redirect('gestion:empleados-listar')

	context = {'form':form}
	return render(request, 'empleados/modificar.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='delete_empleado')
def borrar_empleado(request, pk):
	empleado = Empleado.objects.get(id=pk)
	usuario = User.objects.get(username=empleado.usuario.username) 
	if request.method == "POST":
		empleado.delete()
		usuario.delete()
		return redirect('gestion:empleados-listar')

	context = {'empleado':empleado}
	return render(request, 'empleados/borrar.html', context)