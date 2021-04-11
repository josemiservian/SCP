# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Decorador
from scp.decorators import allowed_users

#Modelos
from apps.gestion.models import Area

# Forms
from apps.gestion.forms import FormCrearArea, AreaForm

# Create your views here.

class CrearArea(FormView):
    """ Vista de creacion de Areas"""

    template_name = 'areas/crear.html'
    form_class = FormCrearArea
    success_url = reverse_lazy('gestion:areas-listar')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='empleados/login')
@allowed_users(action='add_area')
def crear_area(request):

	form = FormCrearArea()

	if request.method == 'POST':
		form = FormCrearArea(request.POST)
		if form.is_valid():
			form.save()
			return redirect('gestion:areas-listar')

	context = {'form':form}
	return render(request, 'areas/crear.html', context)

@login_required(login_url='empleados/login')
@allowed_users(action='view_area')
def listar_areas(request):

    areas = Area.objects.all()
    return render(request, 'areas/listar.html', {'areas':areas})


@login_required(login_url='empleados/login')
@allowed_users(action='change_area')
def actualizar_area(request, pk):

	area = Area.objects.get(id=pk)
	form = AreaForm(instance=area)

	if request.method == 'POST':
		form = AreaForm(request.POST, instance=area)
		if form.is_valid():
			form.save()
			return redirect('gestion:areas-listar')

	context = {'form':form}
	return render(request, 'areas/modificar.html', context)


@login_required(login_url='empleados/login')
@allowed_users(action='delete_area')
def borrar_area(request, pk):
	
    area = Area.objects.get(id=pk)
    if request.method == "POST":
        area.delete()
        return redirect('gestion:areas-listar')
        
    context = {'area':area}
    return render(request, 'areas/borrar.html', context)