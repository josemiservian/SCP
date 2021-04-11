# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Decoradores
from scp.decorators import allowed_users

#Modelos
from apps.proyectos.models import Cliente

# Forms
from apps.proyectos.forms import FormCrearCliente, ClienteForm

# Create your views here.

class CrearCliente(FormView):
    """ Vista de creacion de Clientes"""

    template_name = 'clientes/crear.html'
    form_class = FormCrearCliente
    success_url = reverse_lazy('proyectos:clientes-listar')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='empleados/login')
@allowed_users(action='add_cliente')
def crear_cliente(request):

	form = FormCrearCliente

	if request.method == 'POST':
		form = FormCrearCliente(request.POST)
		if form.is_valid():
			form.save()
			return redirect('proyectos:clientes-listar')

	context = {'form':form}
	return render(request, 'clientes/crear.html', context)

@login_required(login_url='empleados/login')
@allowed_users(action='view_cliente')
def listar_clientes(request):

    clientes = Cliente.objects.all()
    return render(request, 'clientes/listar.html', {'clientes':clientes})

@login_required(login_url='empleados/login')
@allowed_users(action='change_cliente')
def actualizar_cliente(request, pk):

	cliente = Cliente.objects.get(id=pk)
	form = ClienteForm(instance=cliente)

	if request.method == 'POST':
		form = ClienteForm(request.POST, instance=cliente)
		if form.is_valid():
			form.save()
			return redirect('proyectos:clientes-listar')

	context = {'form':form}
	return render(request, 'clientes/modificar.html', context)


@login_required(login_url='empleados/login')
@allowed_users(action='delete_cliente')
def borrar_cliente(request, pk):
	
    cliente = Cliente.objects.get(id=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect('proyectos:clientes-listar')
        
    context = {'cliente':cliente}
    return render(request, 'clientes/borrar.html', context)