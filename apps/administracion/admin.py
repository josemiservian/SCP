from django.contrib import admin
from apps.administracion.models import Facturacion, Gasto, Pago

# Register your models here.
admin.site.register(Facturacion)
admin.site.register(Gasto)
admin.site.register(Pago)