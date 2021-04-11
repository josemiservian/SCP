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


class VistaActualizarPerfil(LoginRequiredMixin, UpdateView):

    template_name = 'empleados/configuracion.html'
    model = Empleado
    fields = ['nombre', 'apellido', 'direccion', 'fecha_nacimiento']

    def get_object(self):
        """Retorna perfil del empleado."""
        return self.request.user.empleado

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.usuario.username
        return redirect('')


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