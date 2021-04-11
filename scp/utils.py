from datetime import datetime as dt
from apps.administracion.models import Gasto
from apps.gestion.models import Empleado
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
    print(horas_cargadas)
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

