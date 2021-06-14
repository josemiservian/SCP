# Django
from django import forms

# Models
from django.contrib.auth.models import User, Group, Permission
from django.forms import widgets
from apps.cuentas.models import Empleado
from apps.gestion.models import Cargo

#Python
import datetime

#Constantes
GRUPOS = tuple([(grupo.id, grupo.name) for grupo in Group.objects.all()])
CHOICES = tuple([
    (permiso.id, permiso.content_type.app_label + '|' + permiso.content_type.model + '|' + permiso.name) for permiso in Permission.objects.all()
])

#Formularios para Empleado

class FormularioRegistro(forms.Form):

    username = forms.CharField(min_length=4, max_length=50)
    grupo = forms.ModelChoiceField(queryset=Group.objects.all())

    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput()
    )

    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput()
    )

    cedula = forms.CharField(label= 'Cedula', min_length=5, max_length=20)
    nombre = forms.CharField(label= 'Nombre')
    apellido = forms.CharField(label= 'Apellido')
    direccion = forms.CharField(label= 'Direccion')
    fecha_nacimiento = forms.DateField(label= 'Fecha de Nacimiento', widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    cargo = forms.ModelChoiceField(label= 'Cargo', queryset=Cargo.objects.all())
    tarifa = forms.FloatField(label= 'Tarifa')
    estado = forms.CharField(label= 'Estado')

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use.')
        return username

    def clean_cedula(self):
        '''Valida la unicidad del numero de cedula'''

        cedula = self.cleaned_data.get('cedula')
        
        if Empleado.objects.filter(cedula=cedula).exists():
            raise forms.ValidationError(f'El número de cédula {cedula} ya se encuentra registrado.') 
        return cedula

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')

        return data

    def save(self):
        """Create user and profile."""
        data = self.cleaned_data
        data.pop('password_confirmation')
        user = User.objects.create_user(username=data['username'], password=data['password'], email=data['email'])
        user.groups.add(data['grupo'])
        
        #Si la cantidad de permisos del grupo el cual se le fue asignado
        #al usuario es el total de permisos entonces se le asignara el 
        #estado de "staff" y podrá acceder a la intefaz de administracion
        #de Django
        grupo = Group.objects.filter(pk=data['grupo'].id)

        if grupo[0].permissions.count() == Permission.objects.count():
            user.is_staff = True

        empleado = Empleado(usuario=user, cedula=data['cedula'], nombre=data['nombre'], 
                            apellido=data['apellido'], direccion=data['direccion'], 
                            fecha_nacimiento=data['fecha_nacimiento'], 
                            cargo=data['cargo'], tarifa=data['tarifa'],
                            estado=data['estado'])
        user.save()
        empleado.save()


class EmpleadoForm(forms.ModelForm):
    """Formulario de Empleado."""

    class Meta:
        
        model = Empleado
        fields = ('cedula','nombre', 'apellido', 'direccion', 'fecha_nacimiento')#, 'cargo', 'tarifa', 'estado'
        widgets = {
            'fecha_nacimiento': forms.SelectDateWidget(
                years=range(1900, datetime.date.today().year-17))
            }
