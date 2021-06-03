# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

#Decoradores
from scp.decorators import allowed_users

#Models
from apps.administracion.models import Facturacion, Pago, PlanFacturacion

#Formularios
from apps.administracion.forms import PagoForm, FormCrearPago

#Filtros
from apps.administracion.filtros import PagoFilter

# Create your views here.

class CrearPago(FormView):
    """ Vista de creacion de Pagos"""

    template_name = 'pagos/crear.html'
    form_class = FormCrearPago
    success_url = reverse_lazy('administracion:pagos-listar')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='cuentas:login')
@allowed_users(action='add_pago')
def crear_pago(request):

    form = FormCrearPago

    if request.method == 'POST':
        form = FormCrearPago(request.POST)
        if form.is_valid():
            form.save()
            return redirect('administracion:pagos-listar')

    context = {'form':form}
    return render(request, 'pagos/crear.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_pago')
def listar_pagos(request):

    pagos = Pago.objects.all()
    
    filtros = PagoFilter(request.GET, queryset=pagos)

    pagos = filtros.qs
    
    return render(request, 'pagos/listar.html', {'pagos':pagos, 'filtros':filtros})

@login_required(login_url='cuentas:login')
@allowed_users(action='change_pago')
def actualizar_pago(request, pk):

    pago = Pago.objects.get(id=pk)
    form = PagoForm(instance=pago)

    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            return redirect('administracion:pagos-listar')

    context = {'form':form}
    return render(request, 'pagos/modificar.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='delete_pago')
def borrar_pago(request, pk):
    
    pago = Pago.objects.get(id=pk)
    if request.method == "POST":
        pago.delete()
        return redirect('administracion:pagos-listar')
        
    context = {'pago':pago}
    return render(request, 'pagos/borrar.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_pago')
def detalle_pago(request, pk):

    pago = Pago.objects.get(id=pk)
    plan = PlanFacturacion.objects.get(id=pago.factura.plan_facturacion.id)
    context = {'pago':pago, 'plan':plan}
    return render(request, 'pagos/detalle.html', context)