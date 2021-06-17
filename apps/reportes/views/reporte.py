# Django
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#Decoradores
from scp.decorators import allowed_users

#Modelos
from apps.proyectos.models import Contrato, RegistroHora

#Formularios
from apps.reportes.forms import ReportForm



class ReportHorasView(TemplateView):
    template_name = 'seguimientos/report.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = RegistroHora.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.empleado,
                        s.contrato,
                        s.fecha.strftime('%Y-%m-%d'),
                        s.horas_trabajadas,
                    ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Horas Insumidas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('reportes:Report-Horas')
        context['form'] = ReportForm()
        return context
