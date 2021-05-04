# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory

#Decoradores
from scp.decorators import allowed_users

#Modelos
from apps.proyectos.models import Propuesta, PropuestaDetalle

# Forms
from apps.proyectos.forms import FormCrearPropuesta, PropuestaForm, FormCrearPropuestaDetalle, PropuestaDetalleForm

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
			return redirect(str(pk) + '/detalle/crear')

	context = {'form':form}
	return render(request, 'propuestas/crear.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def listar_propuestas(request, estado):


    propuestas = Propuesta.objects.all()
    
    if estado == 'P':
        propuestas = propuestas.filter(estado='P')
    elif estado == 'A':
        propuestas = propuestas.filter(estado='A')
    else:
        propuestas = propuestas.filter(estado='R')
    
    return render(request, 'propuestas/listar.html', {'propuestas':propuestas, 'estado':estado})

@login_required(login_url='cuentas:login')
@allowed_users(action='change_propuesta')
def actualizar_propuesta(request, pk):

	propuesta = Propuesta.objects.get(id=pk)
	form = PropuestaForm(instance=propuesta)

	if request.method == 'POST':
		form = PropuestaForm(request.POST, instance=propuesta)
		if form.is_valid():
			form.save()
            #form.estado.values()
			return redirect('proyectos:propuestas-listar', form.estado.values())

	context = {'form':form, 'propuesta':pk, 'estado':propuesta.estado}
	return render(request, 'propuestas/modificar.html', context)


@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def detalle_propuesta(request, pk):

    propuesta = Propuesta.objects.get(id=pk)
    return render(request, 'propuestas/detalle.html', {'propuesta':propuesta})

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
            return redirect('proyectos:propuestas-listar', 'P')
            
    context = {'formset':formset}
    return render(request, 'propuestas/crear_propuestaDetalle.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def listar_propuestasDetalle(request):

    propuestas_detalle = PropuestaDetalle.objects.all() #queryset
    return render(request, 'propuestas/listar_propuestaDetalle.html', {'propuestas_detalle':propuestas_detalle})

@login_required(login_url='cuentas:login')
@allowed_users(action='view_propuesta')
def listar_detalle_propuesta(request, pk):
    '''Lista los detalles de propuestas dada una propuesta'''
    propuestas_detalle = PropuestaDetalle.objects.filter(propuesta__id=pk)
    return render(request, 'propuestas/listar_propuestaDetalle.html', {'propuestas_detalle':propuestas_detalle})

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
