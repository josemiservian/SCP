from django.contrib import admin
# Register your models here.

#Models
from django.contrib.auth.models import User
from apps.gestion.models import Area, Cargo, Rol, Servicio


admin.site.register(Area)
admin.site.register(Cargo)
admin.site.register(Rol)
admin.site.register(Servicio)
