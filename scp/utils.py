import datetime
from datetime import datetime as dt
from dateutil import relativedelta

#Modelos
from apps.administracion.models import PlanFacturacion 
from apps.cuentas.models import Empleado
from apps.proyectos.models import Contrato, EquipoProyecto, MiembroEquipoProyecto

def calcular_horas(horas, accion): 
    '''Calcula la diferencia entre dos horas.'''
    
    #contrato = Contrato.objects.filter(id=contrato)[0]
    horas_cargadas = dt.strptime(horas,'%H:%M')
    horas_cargadas = horas_cargadas.hour + horas_cargadas.minute / 60
    if accion == 'INSERT':
        pass
    elif accion == 'UPDATE':
        pass
    elif accion == 'DELETE':

        horas_cargadas = horas_cargadas * -1
    return horas_cargadas


def calcular_gasto_hora(usuario, contrato, horas):
    '''Calcular el monto gasto por las horas trabajadas por el empleado.'''

    gasto = 0
    empleado = Empleado.objects.get(usuario__username=usuario)
    #Se busca al empleado en el proyecto indicado para obtener la tarifa
    #por hora asignada para el proyecto
    equipo = EquipoProyecto.objects.get(contrato__id=contrato)
    #si el empleado es lider de proyecto 
    if EquipoProyecto.objects.filter(contrato__id=contrato).filter(lider_proyecto=empleado):
        gasto = empleado.tarifa * horas
    #Si no es lider del proyecto (pertenece a un squad).
    else:
        miembro = MiembroEquipoProyecto.objects.get(
            empleado__id=empleado.id,
            equipo_proyecto__id=equipo.id
        )
        gasto = miembro.tarifa_asignada * horas
    return gasto


def generar_planes(condicion_pago):
        '''Genera los planes de facturacion basado en la cantidad de pagos.
        Se generará para un contrato tantos planes como cantidad de pagos se tenga'''
        hoy = datetime.date.today()
        cantidad_pagos = condicion_pago.cantidad_pagos
        monto_total = condicion_pago.monto_total
        numero_pago = 1

        while numero_pago <= condicion_pago.cantidad_pagos:
            
            descripcion=condicion_pago.contrato.nombre + ' - ' + f'{numero_pago}/{cantidad_pagos}'
            fecha_emision=hoy+relativedelta.relativedelta(months=numero_pago)
            fecha_vencimiento=fecha_emision+relativedelta.relativedelta(days=10)
            monto_facturar=monto_total/cantidad_pagos

            plan = PlanFacturacion(
                descripcion=descripcion,
                fecha_emision=fecha_emision,
                fecha_vencimiento=fecha_vencimiento,
                monto_facturar=monto_facturar,
                condicion_pago = condicion_pago
            )
            plan.save()

            numero_pago += 1