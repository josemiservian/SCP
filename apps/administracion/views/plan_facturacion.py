# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


#Decoradores
from scp.decorators import allowed_users

#Modelos
from apps.administracion.models import Facturacion

@login_required(login_url='cuentas:login')
@allowed_users(action='change_planfacturacion')
def emitir_facturado(request, pk):
        
    factura = Facturacion.objects.get(plan_facturacion__id=pk)

    if request.method == 'POST':
        factura.save()

        return redirect('proyectos:propuestas-detalle', propuesta.id)
    
    context = {'propuesta':propuesta, 'estado':estado}
    return render(request, 'propuestas/estado_propuesta.html', context)