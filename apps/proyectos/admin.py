from django.contrib import admin
from apps.proyectos.models import Cliente, Contrato, EquipoProyecto, MiembroEquipoProyecto, RegistroHora, Propuesta, PropuestaDetalle

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Contrato)
admin.site.register(EquipoProyecto)
admin.site.register(MiembroEquipoProyecto)
admin.site.register(RegistroHora)
admin.site.register(Propuesta)
admin.site.register(PropuestaDetalle)