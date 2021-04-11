# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import  authenticate, login, logout #views as
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

#Decoradores
from scp.decorators import allowed_users

# Models
from django.contrib.auth.models import User
from apps.gestion.models import Empleado

# Forms
from apps.gestion.forms import FormularioRegistro, EmpleadoForm

class VistaRegistro(FormView):

    template_name = 'empleados/registro.html'
    form_class = FormularioRegistro
    success_url = reverse_lazy('gestion:empleados-login')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


class VistaActualizarPerfil(LoginRequiredMixin, UpdateView):

    template_name = 'empleados/configuracion.html'
    model = Empleado
    fields = ['nombre', 'apellido', 'direccion', 'fecha_nacimiento', 'cargo', 'tarifa', 'estado']

    def get_object(self):
        """Retorna perfil del empleado."""
        return self.request.user.empleado

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.usuario.username
        return reverse('gestion:empleados-inicio')


#FUNCIONES
def vista_login(request):
	if request.user.is_authenticated:
		return redirect('gestion:empleados-inicio')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('gestion:empleados-inicio')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'empleados/login.html', context)


def vista_logout(request):
	logout(request)
	return redirect('gestion:empleados-login')

@login_required(login_url='empleados/login')
def inicio(request):

	return render(request, 'index.html')

@login_required(login_url='empleados/login')
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

@login_required(login_url='empleados/login')
@allowed_users(action='view_empleado')
def listar_empleados(request):

    empleados = Empleado.objects.all().order_by('id')
    return render(request, 'empleados/listar.html', {'empleados':empleados})

@login_required(login_url='empleados/login')
@allowed_users(action='change_empleado')
def actualizar_empleado(request, pk):

	empleado = Empleado.objects.get(id=pk)
	form = EmpleadoForm(instance=empleado)

	if request.method == 'POST':
		form = EmpleadoForm(request.POST, instance=empleado)
		if form.is_valid():
			form.save()
			return redirect('gestion:empleados-listar')

	context = {'form':form}
	return render(request, 'empleados/modificar.html', context)

@login_required(login_url='empleados/login')
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