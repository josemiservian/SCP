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


class VistaActualizarPerfil(LoginRequiredMixin, UpdateView):

    template_name = 'cuentas/configuracion.html'
    model = Empleado
    fields = ['nombre', 'apellido', 'direccion', 'fecha_nacimiento']

    def get_object(self):
        """Retorna perfil del empleado."""
        return self.request.user.empleado

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.usuario.username
        return redirect('cuentas:inicio')


#FUNCIONES
def vista_login(request):
	if request.user.is_authenticated:
		return redirect('cuentas:inicio')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('cuentas:inicio')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'cuentas/login.html', context)


def vista_logout(request):
	logout(request)
	return redirect('cuentas:login')

@login_required(login_url='cuentas:login')
def inicio(request):
	'''Pagina de inicio'''
	if request.user.is_authenticated:
		registro_horas = RegistroHora.objects.filter(
			empleado__usuario__username=request.user).values(
			'contrato__nombre',
			'nombre',
			'detalle',
			'fecha',
			horas=Cast('horas_trabajadas', TimeField()))

		#Últimas 5 tareas cargadas
		tareas_realizadas = registro_horas.values(
			'contrato__nombre', 
			'nombre',
			'detalle',
			'fecha').order_by('fecha')[:5]

		#Horas cargadas por proyecto, en el mes
		horas_proyectos = registro_horas.values('contrato__nombre').annotate(Sum('horas'))

		#Proyectos asignadas en el mes (activos)
		proyectos_asignados = registro_horas.values('contrato__nombre').distinct().count()

		#Total de horas mensuales
		total_horas_mensuales = registro_horas.aggregate(Sum('horas'))
		total_horas_mensuales = total_horas_mensuales['horas__sum']
		total_horas_mensuales = 0 #int(total_horas_mensuales.days *24 + total_horas_mensuales.seconds/3600)

		#Total de tareas realizadas en el mes
		total_tareas_mensuales = registro_horas.values('nombre').distinct().count()

		context = {
			'proyectos_asignados':proyectos_asignados,
			'total_horas_mensuales':total_horas_mensuales,
			'total_tareas_mensuales':total_tareas_mensuales,
			'tareas_realizadas':tareas_realizadas,
			'horas_proyectos':horas_proyectos
		}
		return render(request, 'index.html',context)
	else:
		return redirect('login')

@login_required(login_url='cuentas:login')
def admin(request):
	context = {}
	return render(request, 'inicio.html',context) 


'''@login_required(login_url='cuentas:login')
def resumen(request):

	registro_horas = RegistroHora.objects.filter(
		empleado__usuario__username=request.user).values(
		'contrato__nombre',
		'nombre',
		'detalle',
		'fecha',
		horas=Cast('horas_trabajadas', TimeField()))
	
	#Proyectos asignadas en el mes (activos)
	proyectos_asignados = registro_horas.values('contrato__nombre').distinct().count()

	#Total de horas mensuales
	total_horas_mensuales = registro_horas.aggregate(Sum('horas'))
	total_horas_mensuales = total_horas_mensuales['horas__sum']
	total_horas_mensuales = int(total_horas_mensuales.days *24 + total_horas_mensuales.seconds/3600)

	#Total de tareas realizadas en el mes
	total_tareas_mensuales = registro_horas.values('nombre').distinct().count()

	context = {
		'total_horas_mensuales':total_horas_mensuales,
		'proyectos_asignados':proyectos_asignados,
		'total_tareas_mensuales':total_tareas_mensuales
	}

	return render(request, 'cuentas/resumen.html',context)'''