import datetime
from datetime import datetime as dt
from dateutil import relativedelta

#Modelos
from apps.administracion.models import PlanFacturacion 
from apps.cuentas.models import Empleado
from apps.proyectos.models import Contrato, EquipoProyecto, MiembroEquipoProyecto

def calcular_horas(hora_inicio, hora_fin, accion):#contrato, 
    '''Calcula la diferencia entre dos horas.'''
    
    #contrato = Contrato.objects.filter(id=contrato)[0]
    horas_cargadas = dt.strptime(hora_fin,'%H:%M:%S') - dt.strptime(hora_inicio,'%H:%M:%S')
    if accion == 'INSERT':
        
        horas_cargadas = horas_cargadas.seconds / 3600
        
    elif accion == 'UPDATE':
        pass
    elif accion == 'DELETE':

        horas_cargadas = (horas_cargadas.seconds / 3600) * -1
    
    return horas_cargadas
    #contrato.sumar_horas(horas_cargadas)
    #contrato.save()


def calcular_gasto_hora(usuario, contrato, horas):
    '''Calcular el monto gasto por las horas trabajadas por el empleado.'''

    empleado = Empleado.objects.filter(usuario__username=usuario)[0]
    #Se busca al empleado en el proyecto indicado para obtener la tarifa
    #por hora asignada para el proyecto
    equipo = EquipoProyecto.objects.filter(contrato__id=contrato)[0]
    miembro = MiembroEquipoProyecto.objects.filter(empleado__id=empleado.id,
                                                   equipo_proyecto__id=equipo.id)[0]
    gasto = miembro.tarifa_asignada * horas
    return gasto


def generar_planes(contrato, monto_total, cantidad_pagos):
        '''Genera los planes de facturacion basado en la cantidad de pagos.
        Se generará para un contrato tantos planes como cantidad de pagos se tenga'''
        hoy = datetime.date.today()
        numero_pago = 1

        while numero_pago <= cantidad_pagos:
            
            contrato=contrato
            descripcion=contrato.nombre + ' - ' + f'{numero_pago}/{cantidad_pagos}'
            fecha_emision=hoy+relativedelta.relativedelta(months=numero_pago)
            fecha_vencimiento=fecha_emision+relativedelta.relativedelta(days=10)
            monto_facturar=monto_total/cantidad_pagos

            plan = PlanFacturacion(
                contrato=contrato,
                descripcion=descripcion,
                fecha_emision=fecha_emision,
                fecha_vencimiento=fecha_vencimiento,
                monto_facturar=monto_facturar
            )
            plan.save()

            numero_pago += 1