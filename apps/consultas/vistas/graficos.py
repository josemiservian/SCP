from django.db.models.aggregates import Count
from django.db.models.base import Model
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db.models import F, Func
from django.db.models import Sum, Count, TimeField
from django.db.models.functions import Cast

#formularios
from apps.consultas.forms import  GraficoForm

#Modelos
from apps.proyectos.models import Contrato, RegistroHora, Entregable
from apps.administracion.models import Gasto

class GraficoView(TemplateView):
    template_name = 'c_contratos/graficos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
       
        try:
            action = request.POST['action']
            if action == 'get_graph_hours_year_month':
               data  = {
                   'name': 'Total de gastos',
                   'showInLegend': True,
                   'showlabels': True,
                   'colorByPoint': True,
                   'data': self.get_graph_hours_year_month()
                }
            elif action == 'get_graph_hours_vero_year_month':
                data = {
                    'name': 'Horas Presupuestadas',
                    'colorByPoint': False,
                    'data': self.get_graph_hours_vero_year_month(),
                }
            elif action == 'get_graph_hours_vero2_year_month':
                data = {
                    'name': 'Horas Ejecutadas',
                    'colorByPoint': False,
                    'data': self.get_graph_hours_vero2_year_month(),
                }
               
            elif action == 'get_graph_hours_porproyecto':
                data = {
                    'name': 'Monto del contrato',
                    'colorByPoint': False,
                    'data': self.get_graph_hours_porproyecto(),
                }  
            elif action == 'get_graph_gastos_porproyecto':
                data = {
                    'name': 'Gastos',
                    'colorByPoint': False,
                    'data': self.get_graph_gastos_porproyecto(),
                }   
            elif action == 'get_graph_hours_contrato_year_month':
                data = {
                    'name': 'Desviación de Horas',
                    'colorByPoint': True,
                    'data': self.get_graph_hours_contrato_year_month(),
                }
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    #metodo para calcular el gasto total por contratos
    def get_graph_hours_year_month(self):
        data = []
        year = datetime.now().year
        try:
            for p in Contrato.objects.all():
                total = Gasto.objects.filter(contrato_id = p.id, fecha__year=year).order_by('motivo').aggregate(
                    r=Coalesce(Sum('gasto'), 0)).get('r')
                data.append({
                            'name': p.nombre,
                            'y': float(total),
                            'xAxis': p.nombre,                           
                            #'data': total
                        })
        except:
            pass
        return data
    
     #metodo para calcular las desviaciones de las horas por proyectos
    def get_graph_hours_contrato_year_month(self):
        data = []
        contratos = Contrato.objects.all()
        year = datetime.now().year
        #month = datetime.now().month
        try:
            for contrato in contratos:
                data.append({
                        'name': contrato.nombre,
                        'y': float(contrato.horas_presupuestadas-contrato.horas_ejecutadas),
                    })
        except:
            pass
        print(data)
        return data
    #metodo para calcular el total de horas por proyecto y por mes en el año 2021
    def get_graph_hours_vero_year_month(self):
        data = []
       
        contratos = Contrato.objects.all()
        year = datetime.now().year
        #month = datetime.now().month
        try:
            for contrato in contratos:
                data.append({
                        'name': contrato.nombre,
                        'y': float(contrato.horas_presupuestadas),
                        
                    })
               
              
        except:
            pass
        return data
    
    #Registro de horas por proyectos
    def get_graph_hours_porproyecto(self):
        data = []
       
        contratos = Contrato.objects.all()
        year = datetime.now().year
        

        #month = datetime.now().month
        try:
            for contrato in contratos:
                data.append({
                        'name': contrato.nombre,
                        'y': float(contrato.monto),
                        
                    })
               
              
        except:
            pass
        return data
    
    def get_graph_gastos_porproyecto(self):
        data = []
       
        contratos = Contrato.objects.all()
        year = datetime.now().year
        

        #month = datetime.now().month
        try:
            for contrato in contratos:
                data.append({
                        'name': contrato.nombre,
                        'y': float(contrato.gastos),
                        
                    })
               
              
        except:
            pass
        return data
   
    def get_graph_hours_vero2_year_month(self):
        data = []
       
        contratos = Contrato.objects.all()
        year = datetime.now().year
        #month = datetime.now().month
        try:
            for contrato in contratos:
                data.append({
                        'name': contrato.nombre,
                        'y': float(contrato.horas_ejecutadas),
                        
                    })
               
              
        except:
            pass
        return data
    

    #metodo de calculo de desviación de horas
    def get_desviacion_horas(self):
        data = []
        try:
             query = Contrato.objects.raw('SELECT  * FROM contrato WHERE id = 1')
             data.append(query)
        except:
            pass
        return data

    #metodo para el calculo de la desviación de horas por entregables del proyecto


    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['graph_hours_year_month'] = self.get_graph_hours_year_month()
        context['get_graph_hours_contrato_year_month'] = self.get_graph_hours_contrato_year_month()
        context['graph_hours_vero_year_month'] = self.get_graph_hours_vero_year_month()
        context['graph_hours_vero2_year_month'] = self.get_graph_hours_vero2_year_month()
        context['get_graph_hours_porproyecto'] = self.get_graph_hours_porproyecto() 
        context['get_graph_gastos_porproyecto'] = self.get_graph_gastos_porproyecto()         
        
        
        return context
