# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.utils import timezone

#Utilidades
from scp import utils

#Decoradores
from scp.decorators import allowed_users

#Models
from apps.administracion.models import Gasto
from apps.cuentas.models import Empleado
from apps.proyectos.models import Contrato, RegistroHora

#Formularios
from apps.proyectos.forms import FormCrearRegistroHora, RegistroForm

# Create your views here.

class CrearRegistroHora(FormView):
    """ Vista de creacion de Registro de horas"""

    template_name = 'registroHoras/crear.html'
    form_class = FormCrearRegistroHora
    success_url = reverse_lazy('proyectos:registrohoras-listar')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)


#FUNCIONES
@login_required(login_url='cuentas:login')
@allowed_users(action='add_registrohora')
def crear_registroHoras(request):

    form = FormCrearRegistroHora()

    if request.method == 'POST':
        form = FormCrearRegistroHora(request.POST)
        if form.is_valid():
            #Aumenta la cantidad de horas cargadas a las HORAS EJECUTADAS,
            #las tarifas por hora de los empleado a GASTO y calcula la
            #RENTABILIDAD (en horas y presupuesto) del Contrato
            contrato = Contrato.objects.filter(id=form['contrato'].value())[0]
            horas = utils.calcular_horas(
                
                form['hora_inicio'].value(), 
                form['hora_fin'].value(),
                'INSERT'
            )
            gastos = utils.calcular_gasto_hora(request.user, contrato.id, horas)
            contrato.maestro_calculos(horas, gastos)
            contrato.save()
            registro_id = form.save(request)
            gasto_horas = Gasto.objects.create(
                motivo='HONORARIOS', 
                detalle=form['detalle'].value(),
                fecha=form['fecha'].value(),
                gasto=utils.calcular_gasto_hora(request.user, contrato.id, horas),
                empleado_id=Empleado.objects.filter(usuario__username=request.user)[0].id,
                contrato_id=contrato.id,
                registro_id=registro_id
            )
            gasto_horas.save()

            return redirect('proyectos:registrohoras-listar')

    context = {'form':form}
    return render(request, 'registroHoras/crear.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_registrohora')
def listar_registroHoras(request):
    '''Lista las horas cargadas por el usuario '''
    registros = RegistroHora.objects.filter(empleado__usuario__username=request.user)
    return render(request, 'registroHoras/listar.html', {'registros':registros})        

@login_required(login_url='cuentas:login')
@allowed_users(action='change_registrohora')
def actualizar_registroHora(request, pk):

    registro = RegistroHora.objects.get(id=pk)
    form = RegistroForm(instance=registro)

    if request.method == 'POST':
        #Se utilizara la accion DELETE para borrar la anterior hora cargada
        contrato = Contrato.objects.filter(id=form['contrato'].value())[0]
        horas_anteriores = utils.calcular_horas(
            
            str(form['hora_inicio'].value()), 
            str(form['hora_fin'].value()),
            'DELETE'
        )
        gastos = utils.calcular_gasto_hora(request.user, contrato.id, horas_anteriores)
        contrato.sumar_horas(horas_anteriores)
        contrato.sumar_gastos(gastos)
        contrato.save()

        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            #Se utilizara la accion INSERT para cargar las horas actualizadas
            contrato = Contrato.objects.filter(id=form['contrato'].value())[0]
            gasto_horas = Gasto.objects.filter(registro__id=pk)[0]
            horas = utils.calcular_horas(
                
                form['hora_inicio'].value(), 
                form['hora_fin'].value(),
                'INSERT'
            )

            gastos = utils.calcular_gasto_hora(request.user, contrato.id, horas)
            contrato.maestro_calculos(horas, gastos)
            gasto_horas.gasto = gastos
            gasto_horas.save()
            contrato.save()
            form.save()
            return redirect('proyectos:registrohoras-listar')

    context = {'form':form}
    return render(request, 'registroHoras/modificar.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='delete_registrohora')
def borrar_registroHora(request, pk):

    registro = RegistroHora.objects.get(id=pk)
    if request.method == "POST":
        contrato = Contrato.objects.filter(id=registro.contrato.id)[0]
        horas = utils.calcular_horas(
                registro.hora_inicio.strftime('%H:%M:%S'),
                registro.hora_fin.strftime('%H:%M:%S'),
                'DELETE'
            )
        gastos = utils.calcular_gasto_hora(request.user, contrato.id, horas)
        contrato.maestro_calculos(horas, gastos)
        gasto_horas = Gasto.objects.filter(registro__id=pk)
        contrato.save()
        gasto_horas.delete()
        registro.delete()
        return redirect('proyectos:registrohoras-listar')
        
    context = {'registro':registro}
    return render(request, 'registroHoras/borrar.html', context)

@login_required(login_url='cuentas:login')
@allowed_users(action='view_registrohora')
def resumen_horas_empleado(request):
    '''Resumen de horas trabajadas totales del empleado.'''
    pass