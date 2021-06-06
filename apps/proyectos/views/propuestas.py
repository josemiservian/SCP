# Django
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
from apps.administracion.models import Gasto
from apps.proyectos.models import Propuesta, PropuestaDetalle

# Forms
from apps.proyectos.forms import FormCrearPropuesta, PropuestaForm, PropuestaDetalleForm, PropuestaAsociarCliente
from apps.administracion.forms import FormCrearGasto

#Filtros
from apps.proyectos.filtros import PropuestaFilter

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

#Propuesta
@login_required(login_url='cuentas:login')
@allowed_users(action='add_propuesta')
def crear_propuesta(request):

    form = FormCrearPropuesta

    if request.method == 'POST':
        form = FormCrearPropuesta(request.POST)
        if form.is_valid():
            pk = form.save()
            return redirect('proyectos:propuestas-listar', 'P')
            #return redirect(str(pk) + '/detalle/crear')

    context = {'form':form}
    return render(request, 'propuestas/crear.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def listar_propuestas(request, estado):

    propuestas = Propuesta.objects.all() #queryset

    filtros = PropuestaFilter(request.GET, queryset=propuestas)

    propuestas = filtros.qs

    paginator = Paginator(propuestas, 10)

    page = request.GET.get('page')

    propuestas = paginator.get_page(page)


    #return render(request, 'propuestas/listar.html', {'propuestas':propuestas, 'filtros':filtros})
    

    #propuestas = Propuesta.objects.all()
    
    if estado == 'P':
        propuestas = propuestas.filter(estado='P')
    elif estado == 'A':
        propuestas = propuestas.filter(estado='A')
    else:
        propuestas = propuestas.filter(estado='R')
    
    return render(request, 'propuestas/listar.html', {'propuestas':propuestas, 'estado':estado, 'filtros':filtros})

@login_required(login_url='cuentas:login')
@allowed_users(action='change_propuesta')
def actualizar_propuesta(request, pk):

    propuesta = Propuesta.objects.get(id=pk)
    form = PropuestaForm(instance=propuesta)

    if request.method == 'POST':
        form = PropuestaForm(request.POST, instance=propuesta)
        if form.is_valid():
            form.save()
            return redirect('proyectos:propuestas-detalle', propuesta.id)

    context = {'form':form, 'propuesta':pk}
    return render(request, 'propuestas/modificar.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def detalle_propuesta(request, pk):

    propuesta = Propuesta.objects.get(id=pk)
    return render(request, 'propuestas/detalle.html', {'propuesta':propuesta})

@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def propuesta_json(request, pk):
    '''Retorna una propuesta dada en formato JSON'''
    
    propuesta = list(Propuesta.objects.filter(id=pk).values(
        'id', 
        'nombre', 
        'horas_totales', 
        'ganancia_esperada'
    ))
    return JsonResponse(propuesta, safe=False)

@login_required(login_url='cuentas:login')
@allowed_users(action='add_cliente')
def asociar_cliente_propuesta(request, pk):

    propuesta = Propuesta.objects.get(id=pk)
    form = PropuestaAsociarCliente

    if request.method == 'POST':
        form = PropuestaAsociarCliente(request.POST)
        if form.is_valid():
            form.save(pk)
            return redirect('proyectos:propuestas-detalle', pk)

    context = {'form':form, 'propuesta':propuesta}
    return render(request, 'propuestas/asociar_cliente.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def estado_propuesta(request, pk, estado):
        
    propuesta = Propuesta.objects.get(id=pk)

    if request.method == 'POST':
        propuesta.definir_estado(estado)
        propuesta.save()
        return redirect('proyectos:propuestas-detalle', propuesta.id)
    
    context = {'propuesta':propuesta, 'estado':estado}
    return render(request, 'propuestas/estado_propuesta.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='delete_propuesta')
def borrar_propuesta(request, pk):
    
    propuesta = Propuesta.objects.get(id=pk)
    if request.method == "POST":
        estado = propuesta.estado
        propuesta.delete()
        return redirect('proyectos:propuestas-listar', estado)
        
    context = {'propuesta':propuesta}
    return render(request, 'propuestas/borrar.html', context)

#Propuesta Detalle
@login_required(login_url='cuentas:login')
@allowed_users(action='add_propuestadetalle')
def crear_propuestaDetalle(request, pk):
    
    PropuestaDetalleFormSet = inlineformset_factory(
        Propuesta, 
        PropuestaDetalle,
        fields=('servicio', 'descripcion', 'horas_servicio','cargo','tarifa','total'),
        can_delete=False,
        extra=5
    )
    propuesta = Propuesta.objects.get(id=pk)
    formset = PropuestaDetalleFormSet(
        queryset=PropuestaDetalle.objects.none(),
        instance=propuesta
    )
    if request.method =='POST':
        formset = PropuestaDetalleFormSet(request.POST, instance=propuesta)
        if formset.is_valid():
            formset.save()
            propuesta.calcular_totales()
            propuesta.save()
            return redirect('proyectos:propuestas-detalle', pk)
            
    context = {'formset':formset, 'propuesta':propuesta}
    return render(request, 'propuestas/crear_propuestaDetalle.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def listar_propuestasDetalle(request):

    propuestas_detalle = PropuestaDetalle.objects.all() #queryset
    propuesta = propuestas_detalle[0].id
    context = {'propuestas_detalle':propuestas_detalle, 'propuesta':propuesta}
    return render(request, 'propuestas/listar_propuestaDetalle.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def listar_detalle_propuesta(request, pk):
    '''Lista los detalles de propuestas dada una propuesta'''
    propuestas_detalle = PropuestaDetalle.objects.filter(propuesta__id=pk)
    context = {'propuestas_detalle':propuestas_detalle, 'propuesta':pk}
    return render(request, 'propuestas/listar_propuestaDetalle.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='change_propuesta')
def actualizar_propuestaDetalle(request, pk):

    propuestas_detalle = PropuestaDetalle.objects.get(id=pk)
    form = PropuestaDetalleForm(instance=propuestas_detalle)

    if request.method == 'POST':
        form = PropuestaDetalleForm(request.POST, instance=propuestas_detalle)
        if form.is_valid():
            propuesta = Propuesta.objects.get(id=propuestas_detalle.propuesta.id)
            form.save()
            propuesta.calcular_totales()
            propuesta.save()
            return redirect('proyectos:propuestas-listar', 'P')

    context = {'form':form}
    return render(request, 'propuestas/modificar_propuestaDetalle.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='delete_propuesta')
def borrar_propuestaDetalle(request, pk):
    
    propuesta_detalle = PropuestaDetalle.objects.get(id=pk)
    if request.method == "POST":
        propuesta = Propuesta.objects.get(id=propuesta_detalle.propuesta.id)
        propuesta_detalle.delete()
        propuesta.calcular_totales()
        propuesta.save()
        return redirect('proyectos:propuestasDetalle-detallePorPropuesta', propuesta.id)
        
    context = {'propuesta_detalle':propuesta_detalle, 'propuesta':propuesta_detalle.propuesta.id}
    return render(request, 'propuestas/borrar_propuestaDetalle.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='add_gasto')
def crear_gastos(request, pk):
    '''Gastos asociados a una propuesta.'''

    GastoFormSet = inlineformset_factory(
        Propuesta, 
        Gasto,
        fields=('motivo', 'detalle', 'gasto'),
        can_delete=False,
        extra=5
    )
    propuesta = Propuesta.objects.get(id=pk)
    formset = GastoFormSet(
        queryset=Gasto.objects.none(),
        instance=propuesta
    )
    if request.method =='POST':
        formset = GastoFormSet(request.POST, instance=propuesta)
        if formset.is_valid():
            formset.save()
            propuesta.calcular_totales()
            propuesta.save()
            return redirect('proyectos:propuestas-detalle', pk)
            
    context = {'formset':formset, 'propuesta':propuesta}
    return render(request, 'propuestas/agregar_gasto.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='view_gasto')
def listar_propuestas_gastos(request, pk):
    '''Gastos relacionados a una propuesta'''
    gastos = Gasto.objects.filter(propuesta__id=pk) #queryset
    context = {'gastos':gastos, 'propuesta':pk}
    return render(request, 'propuestas/listar_gastos.html', context)