# Django
from apps.proyectos.models import Contrato
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Decoradores
from scp.decorators import allowed_users

#Models
from apps.administracion.models import Gasto
from apps.proyectos.models import Contrato

#Formularios
from apps.administracion.forms import GastoForm, FormCrearGasto

#Filtros
from apps.administracion.filtros import GastoFilter

# Create your views here.

class CrearGasto(FormView):
    """ Vista de creacion de gastos"""

    template_name = 'gastos/crear.html'
    form_class = FormCrearGasto
    success_url = reverse_lazy('administracion:gastos-listar')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='cuentas:login')
@allowed_users(action='add_gasto')
def crear_gasto(request):

    form = FormCrearGasto

    if request.method == 'POST':
        form = FormCrearGasto(request.POST)
        if form.is_valid():
            gasto = form.save()
            gasto.contrato.maestro_calculos(0, gasto.gasto)
            gasto.contrato.save()
            return redirect('administracion:gastos-listar')

    context = {'form':form}
    return render(request, 'gastos/crear.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_gasto')
def listar_gastos(request):

    gastos = Gasto.objects.all()
    
    filtros = GastoFilter(request.GET, queryset=gastos)

    gastos = filtros.qs
    
    return render(request, 'gastos/listar.html', {'gastos':gastos, 'filtros':filtros})

@login_required(login_url='cuentas:login')
@allowed_users(action='change_gasto')
def actualizar_gasto(request, pk):

    gasto = Gasto.objects.get(id=pk)
    form = GastoForm(instance=gasto)
    gasto.contrato.maestro_calculos(0, -gasto.gasto)
    gasto.contrato.save()
    
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            monto = form['gasto'].value()
            gasto.contrato.maestro_calculos(0, monto)
            gasto.contrato.save()
            form.save()
            return redirect('administracion:gastos-listar')

    context = {'form':form}
    return render(request, 'gastos/modificar.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='delete_gasto')
def borrar_gasto(request, pk):
    
    gasto = Gasto.objects.get(id=pk)
    if request.method == "POST":
        gasto.contrato.maestro_calculos(0, -gasto.gasto)
        gasto.contrato.save()
        gasto.delete()
        return redirect('administracion:gastos-listar')
        
    context = {'gasto':gasto}
    return render(request, 'gastos/borrar.html', context)
