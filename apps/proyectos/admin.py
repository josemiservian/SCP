#Django
from django.contrib import admin
from django.contrib.admin import site as admin_site

#Modelos y formularios
from apps.proyectos.models import Cliente, Contrato, Entregable, CondicionPago, EquipoProyecto, MiembroEquipoProyecto, RegistroHora, Propuesta, PropuestaDetalle
from apps.proyectos.forms import *

# Register your models here.

class PropuestaAdmin(admin.ModelAdmin):

    form = PropuestaAsociarCliente

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site 
        super(PropuestaAsociarCliente, self).__init__(model, admin_site)

admin.site.register(Cliente)
admin.site.register(Contrato)
admin.site.register(Entregable)
admin.site.register(CondicionPago)
admin.site.register(EquipoProyecto)
admin.site.register(MiembroEquipoProyecto)
admin.site.register(RegistroHora)
admin.site.register(Propuesta)
admin.site.register(PropuestaDetalle)