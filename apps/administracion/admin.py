from django.contrib import admin
from apps.administracion.models import Facturacion, Gasto, Pago

# Register your models here.
@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    """Gasto admin."""

    list_display = ('pk', 'motivo', 'fecha', 'empleado', 'contrato')
    list_display_links = ('pk', 'motivo','empleado', 'contrato')
    

admin.site.register(Facturacion)
#admin.site.register(Gasto)
admin.site.register(Pago)