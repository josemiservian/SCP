# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Decoradores
from scp.decorators import allowed_users

#Modelos
from apps.proyectos.models import Propuesta, PropuestaDetalle

# Forms
from apps.proyectos.forms import FormCrearPropuesta, PropuestaForm

# Create your views here.

class Crearpropuesta(FormView):
    """ Vista de creacion de propuestas"""

    template_name = 'propuestas/crear.html'
    form_class = FormCrearPropuesta
    success_url = reverse_lazy('proyectos:propuestas-listar')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='cuentas:login')
@allowed_users(action='add_propuesta')
def crear_propuesta(request):

	form = FormCrearPropuesta

	if request.method == 'POST':
		form = FormCrearPropuesta(request.POST)
		if form.is_valid():
			form.save()
			return redirect('proyectos:propuestas-listar')

	context = {'form':form}
	return render(request, 'propuestas/crear.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def listar_propuestas(request):

    propuestas = Propuesta.objects.all() #queryset
    return render(request, 'propuestas/listar.html', {'propuestas':propuestas})

@login_required(login_url='cuentas:login')
@allowed_users(action='change_propuesta')
def actualizar_propuesta(request, pk):

	propuesta = Propuesta.objects.get(id=pk)
	form = PropuestaForm(instance=propuesta)

	if request.method == 'POST':
		form = PropuestaForm(request.POST, instance=propuesta)
		if form.is_valid():
			form.save()
			return redirect('proyectos:propuestas-listar')

	context = {'form':form}
	return render(request, 'propuestas/modificar.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='delete_propuesta')
def borrar_propuesta(request, pk):
	
    propuesta = Propuesta.objects.get(id=pk)
    if request.method == "POST":
        propuesta.delete()
        return redirect('proyectos:propuestas-listar')
        
    context = {'propuesta':propuesta}
    return render(request, 'propuestas/borrar.html', context)
