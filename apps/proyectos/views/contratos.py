# Django
from scp import utils
from apps.administracion.models import PlanFacturacion
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory
from django.core.paginator import Paginator
from django.http import JsonResponse

#Decoradores
from scp.decorators import allowed_users

#Modelos
from apps.proyectos.models import Contrato, Entregable, CondicionPago

#Filtros
from apps.proyectos.filtros import ContratoFilter

# Forms
from apps.proyectos.forms import FormCrearContrato, ContratoForm, EntregableForm, CondicionPagoForm, CondicionPagoFormset, FormCondicionPago

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

#Contratos
'''
@login_required(login_url='cuentas:login')
@allowed_users(action='add_contrato')
def crear_contrato2(request):

    form = FormCrearContrato

    if request.method == 'POST':
        form = FormCrearContrato(request.POST)
        if form.is_valid():
            context = {'form':contrato_creado}
            return render(request, 'contratos/crear.html', context)

    context = {'form':form}
    return render(request, 'contratos/crear.html', context)
'''

@login_required(login_url='cuentas:login')
@allowed_users(action='add_contrato')
def crear_contrato(request):

    form = FormCrearContrato

    if request.method == 'POST':
        form = FormCrearContrato(request.POST)
        if form.is_valid():
            pk = form.save()
            return redirect(f'{pk}/entregables/crear')

    context = {'form':form}
    return render(request, 'contratos/crear.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_contrato')
def detalle_contrato(request, pk):

    contrato = Contrato.objects.get(id=pk)
    return render(request, 'contratos/detalle.html', {'contrato':contrato})

@login_required(login_url='cuentas:login')
@allowed_users(action='view_contrato')
def listar_contratos(request):

    contratos = Contrato.objects.all()
    
    filtros = ContratoFilter(request.GET, queryset=contratos)

    contratos = filtros.qs

    paginator = Paginator(contratos, 10)

    page = request.GET.get('page')

    contratos = paginator.get_page(page)
    
    return render(request, 'contratos/listar.html', {'contratos':contratos, 'filtros':filtros})

@login_required(login_url='cuentas:login')
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

@login_required(login_url='cuentas:login')
@allowed_users(action='delete_contrato')
def borrar_contrato(request, pk):
    
    contrato = Contrato.objects.get(id=pk)
    if request.method == "POST":
        contrato.delete()
        return redirect('proyectos:contratos-listar')
        
    context = {'contrato':contrato}
    return render(request, 'contratos/borrar.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def contrato_json(request, pk):
    '''Retorna una propuesta dada en formato JSON'''
    
    contrato = list(Contrato.objects.filter(id=pk).values(
        'id', 
        'cliente', 
        'monto', 
    ))
    return JsonResponse(contrato, safe=False)


#Entregables del Contrato
@login_required(login_url='cuentas:login')
@allowed_users(action='add_entregable')
def crear_entregable(request, pk):
    
    EntregableFormSet = inlineformset_factory(
        Contrato, 
        Entregable,
        fields=(
            'actividades', 
            'horas_asignadas',
            'fecha_inicio',
            'fecha_fin'
        ),
        can_delete=False,
        extra=5
    )
    contrato = Contrato.objects.get(id=pk)
    formset = EntregableFormSet(
        queryset=Entregable.objects.none(),
        instance=contrato
    )
    if request.method =='POST':
        formset = EntregableFormSet(request.POST, instance=contrato)
        if formset.is_valid():
            formset.save()
            return redirect('proyectos:condicionPagos-crear', contrato.id)
            
    context = {'formset':formset, 'contrato':contrato.id}
    return render(request, 'entregables/crear.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_entregable')
def detalle_entregable(request, pk):

    entregable = Entregable.objects.get(id=pk)
    return render(request, 'entregables/detalle.html', {'entregable':entregable})

@login_required(login_url='cuentas:login')
@allowed_users(action='view_entregable')
def listar_entregables(request, pk):

    entregables = Entregable.objects.filter(contrato__id=pk)

    contrato = Contrato.objects.get(id=pk)
    
    #filtros = entregableFilter(request.GET, queryset=entregables)

    #entregables = filtros.qs

    #paginator = Paginator(entregables, 10)

    #page = request.GET.get('page')

    #entregables = paginator.get_page(page)
    
    return render(request, 'entregables/listar.html', {'entregables':entregables, 'contrato':contrato.id})#, 'filtros':filtros

@login_required(login_url='cuentas:login')
@allowed_users(action='change_entregable')
def actualizar_entregable(request, pk):

    entregable = Entregable.objects.get(id=pk)
    form = EntregableForm(instance=entregable)

    if request.method == 'POST':
        form = EntregableForm(request.POST, instance=entregable)
        if form.is_valid():
            form.save()
            return redirect('proyectos:entregables-detalle', entregable.id)

    context = {'form':form, 'entregable':entregable}
    return render(request, 'entregables/modificar.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='delete_entregable')
def borrar_entregable(request, pk):
    
    entregable = Entregable.objects.get(id=pk)
    if request.method == "POST":
        entregable.delete()
        return redirect('proyectos:entregables-listar')
        
    context = {'entregable':entregable}
    return render(request, 'entregables/borrar.html', context)


#Condiciones de pago del Contrato
@login_required(login_url='cuentas:login')
@allowed_users(action='add_condicionpago')
def crear_condicionPago(request, pk):
    
    form = FormCondicionPago
    contrato = Contrato.objects.get(id=pk)
    form = FormCondicionPago(initial={'contrato': contrato})
    if request.method == 'POST':
        form = FormCondicionPago(request.POST)
        if form.is_valid():
            condicion_pago = form.save(contrato)
            utils.generar_planes(condicion_pago)
            return redirect('proyectos:contratos-detalle', pk)

    context = {'form':form}
    
    return render(request, 'condicionPagos/crear2.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='add_condicionpago')
def crear_condicionPago3(request, pk):
    
    CondicionPagoFormSet = inlineformset_factory(
        Contrato, 
        CondicionPago,
        fields=(
            'forma_pago', 
            'monto_total', 
            'cantidad_pagos',
            'dias_vencimiento'
        ),
        can_delete=False,
        extra=1
    )
    contrato = Contrato.objects.get(id=pk)
    formset = CondicionPagoFormSet(
        queryset=CondicionPago.objects.none(),
        instance=contrato
    )
    if request.method =='POST':
        formset = CondicionPagoFormSet(request.POST, instance=contrato)
        if formset.is_valid():
            formset.save()
            return redirect('proyectos:contratos-detalle', contrato.id)
            
    context = {'formset':formset, 'contrato':contrato.id}
    return render(request, 'condicionPagos/crear2.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='add_condicionpago')
def crear_condicionPago2(request, pk):
    
    contrato = Contrato.objects.get(id=pk)
    if request.method == 'POST':
        print('post')
        formset = CondicionPagoFormset(request.POST)
        for form in formset.forms:
            print("You've picked {0}").format(form.cleaned_data['forma_pago'])
    else:
        print('get')
        formset = CondicionPagoFormset()
    return render(request, 'condicionPagos/crear.html', {'formset': formset, 'contrato':contrato.id})

@login_required(login_url='cuentas:login')
@allowed_users(action='view_condicionpago')
def detalle_condicionPago(request, pk):
    
    condicion = CondicionPago.objects.get(id=pk)
    return render(request, 'condicionPagos/detalle.html', {'condicion':condicion})

@login_required(login_url='cuentas:login')
@allowed_users(action='view_condicionpago')
def listar_condicionPagos(request, pk):
    '''Detalles de condiciones de pago por Contrato'''
    
    condiciones = CondicionPago.objects.filter(contrato__id=pk)
    contrato = Contrato.objects.get(id=pk)
    planes_facturacion = PlanFacturacion.objects.filter(condicion_pago__contrato__id=pk)

    context = {'condiciones':condiciones, 'contrato':contrato}#, 'planes_facturacion':planes_facturacion
    
    return render(request, 'condicionPagos/listar.html', context)#, 'filtros':filtros

@login_required(login_url='cuentas:login')
@allowed_users(action='change_condicionpago')
def actualizar_condicionPago(request, pk):

    condicion = CondicionPago.objects.get(id=pk)
    form = CondicionPagoForm(instance=condicion)

    if request.method == 'POST':
        form = CondicionPagoForm(request.POST, instance=condicion)
        if form.is_valid():
            form.save()
            return redirect('proyectos:condicionPagos-listar')

    context = {'form':form}
    return render(request, 'condicionpagos/modificar.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='delete_condicionpago')
def borrar_condicionPago(request, pk):
    
    condicion = CondicionPago.objects.get(id=pk)
    if request.method == "POST":
        condicion.delete()
        return redirect('proyectos:condicionPagos-listar')
        
    context = {'condicion':condicion}
    return render(request, 'condicionPagos/borrar.html', context)