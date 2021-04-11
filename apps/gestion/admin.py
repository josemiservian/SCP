from django.contrib import admin
# Register your models here.

#Models
from django.contrib.auth.models import User
from apps.gestion.models import Area, Cargo, Empleado, Rol, Servicio

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    """Profile admin."""

    list_display = ('pk', 'usuario', 'cedula', 'nombre', 'apellido')
    list_display_links = ('pk', 'usuario', 'cedula')
    list_editable = ('nombre', 'apellido')

    search_fields = (
        'usuario__email',
        'usuario__username',
        'cedula'
    )

    list_filter = (
        'usuario__is_active',
        'usuario__is_staff',
        'created',
        'modified',
    )

    fieldsets = (
        ('Empleado', {
            'fields': (
                ('usuario'), 
                ('cedula'), 
                ('nombre'), 
                ('apellido'),),
        }),
        ('Extra info', {
            'fields': (
                ('direccion', 'fecha_nacimiento'),
                ('cargo', 'tarifa'),
                ('estado')
            )
        }),
        ('Metadata', {
            'fields': (('created', 'modified'),),
        })
    )

    readonly_fields = ('created', 'modified',)

admin.site.register(Area)
admin.site.register(Cargo)
admin.site.register(Rol)
admin.site.register(Servicio)
