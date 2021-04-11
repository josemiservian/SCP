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
from apps.gestion.models import Empleado
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
@login_required(login_url='empleados/login')
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
            gasto_horas = Gasto.objects.create(
                motivo='HONORARIOS', 
                detalle=form['detalle'].value(),
                fecha=form['fecha'].value(),
                gasto=utils.calcular_gasto_hora(request.user, contrato.id, horas),
                empleado_id=Empleado.objects.filter(usuario__username=request.user)[0].id,
                contrato_id=contrato.id
            )
            gasto_horas.save()
            contrato.save()
            
            form.save(request)
            #return redirect('proyectos:registrohoras-listar')
            return listar_registroHoras(request, request.user)

    context = {'form':form}
    return render(request, 'registroHoras/crear.html', context)


@login_required(login_url='empleados/login')
@allowed_users(action='view_registrohora')
def listar_registroHoras(request, empleado__usuario__username):
    '''Lista las horas cargadas por el usuario '''
    if empleado__usuario__username == request.user:
        registros = RegistroHora.objects.filter(empleado__usuario__username=empleado__usuario__username)
        return render(request, 'registroHoras/listar.html', {'registros':registros})
        
    else:
        registros = RegistroHora.objects.filter(empleado__usuario__username=request.user)
        return render(request, 'registroHoras/listar.html', {'registros':registros})


login_required(login_url='empleados/login')
@allowed_users(action='view_registrohora')
def listar2(request):
    '''Lista las horas cargadas por el usuario '''
    registros = RegistroHora.objects.filter(empleado__usuario__username=request.user)
    return render(request, 'registroHoras/listar.html', {'registros':registros})        

@login_required(login_url='empleados/login')
@allowed_users(action='change_registrohora')
def actualizar_registroHora(request, pk):

    registro = RegistroHora.objects.get(id=pk)
    form = RegistroForm(instance=registro)

    if request.method == 'POST':
        #Se utilizara la accion DELETE para borrar la anterior hora cargada
        contrato = Contrato.objects.filter(id=form['contrato'].value())[0]
        horas = utils.calcular_horas(
            
            str(form['hora_inicio'].value()), 
            str(form['hora_fin'].value()),
            'DELETE'
        )
        gasto_horas = Gasto.objects.create(
            motivo='HONORARIOS', 
            detalle=registro.detalle,
            gasto=utils.calcular_gasto_hora(request.user, registro.contrato.id, horas),
            empleado_id=Empleado.objects.filter(usuario__username=request.user)[0].id,
            contrato_id=registro.contrato.id
        )
        gastos = utils.calcular_gasto_hora(request.user, contrato.id, horas)
        contrato.maestro_calculos(horas, gastos)
        #contrato.save()
        gasto_horas.save()

        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            #Se utilizara la accion INSERT para cargar las horas actualizadas
            horas = utils.calcular_horas(
                
                form['hora_inicio'].value(), 
                form['hora_fin'].value(),
                'INSERT'
            )
            gasto_horas = Gasto.objects.create(
                motivo='HONORARIOS', 
                detalle=form['detalle'].value(),
                fecha=form['fecha'].value(),
                gasto=utils.calcular_gasto_hora(request.user, contrato.id, horas),
                empleado_id=Empleado.objects.filter(usuario__username=request.user)[0].id,
                contrato_id=contrato.id
            )
            contrato = Contrato.objects.filter(id=form['contrato'].value())[0]
            #contrato.sumar_horas(horas)
            #contrato.save()
            gastos = utils.calcular_gasto_hora(request.user, contrato.id, horas)
            contrato.maestro_calculos(horas, gastos)
            gasto_horas.save()
            form.save()
            return listar_registroHoras(request, request.user)

    context = {'form':form}
    return render(request, 'registroHoras/modificar.html', context)


@login_required(login_url='empleados/login')
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
        '''contrato.sumar_horas(horas)
        contrato.sumar_gastos(gastos)
        contrato.calcular_rentabilidad_horas()
        contrato.calcular_rentabilidad_presupuesto()'''

        gasto_horas = Gasto.objects.create(
            motivo='HONORARIOS', 
            detalle=registro.detalle,
            gasto=utils.calcular_gasto_hora(request.user, registro.contrato.id, horas),
            empleado_id=Empleado.objects.filter(usuario__username=request.user)[0].id,
            contrato_id=registro.contrato.id
        )
        
        contrato.save()
        gasto_horas.save()
        registro.delete()
        return redirect('proyectos:registrohoras-listar2')
        
    context = {'registro':registro}
    return render(request, 'registroHoras/borrar.html', context)
