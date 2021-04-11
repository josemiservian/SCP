# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Decoradores
from scp.decorators import allowed_users

#Modelos
from apps.proyectos.models import Contrato

# Forms
from apps.proyectos.forms import FormCrearContrato, ContratoForm

# Create your views here.

class CrearContrato(FormView):
    """ Vista de creacion de Contratos"""

    template_name = 'contratos/crear.html'
    form_class = FormCrearContrato
    success_url = reverse_lazy('proyectos:contratos-listar')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='empleados/login')
@allowed_users(action='add_contrato')
def crear_contrato(request):

	form = FormCrearContrato

	if request.method == 'POST':
		form = FormCrearContrato(request.POST)
		if form.is_valid():
			form.save()
			return redirect('proyectos:contratos-listar')

	context = {'form':form}
	return render(request, 'contratos/crear.html', context)

@login_required(login_url='empleados/login')
@allowed_users(action='view_contrato')
def listar_contratos(request):

    contratos = Contrato.objects.all()
    return render(request, 'contratos/listar.html', {'contratos':contratos})

@login_required(login_url='empleados/login')
@allowed_users(action='change_contrato')
def actualizar_contrato(request, pk):

	contrato = Contrato.objects.get(id=pk)
	form = ContratoForm(instance=contrato)

	if request.method == 'POST':
		form = ContratoForm(request.POST, instance=contrato)
		if form.is_valid():
			form.save()
			return redirect('proyectos:contratos-listar')

	context = {'form':form}
	return render(request, 'contratos/modificar.html', context)


@login_required(login_url='empleados/login')
@allowed_users(action='delete_contrato')
def borrar_contrato(request, pk):
	
    contrato = Contrato.objects.get(id=pk)
    if request.method == "POST":
        contrato.delete()
        return redirect('proyectos:contratos-listar')
        
    context = {'contrato':contrato}
    return render(request, 'contratos/borrar.html', context)
