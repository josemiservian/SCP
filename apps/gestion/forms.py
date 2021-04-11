# Django
from django import forms

# Models
from django.contrib.auth.models import User, Group, Permission
from apps.gestion.models import Area, Empleado, Rol, Servicio

#Constantes
GRUPOS = tuple([(grupo.id, grupo.name) for grupo in Group.objects.all()])
CHOICES = tuple([
    (permiso.id, permiso.content_type.app_label + '|' + permiso.content_type.model + '|' + permiso.name) for permiso in Permission.objects.all()
])


#Formularios para Area
class FormCrearArea(forms.Form):
    
    nombre = forms.CharField(min_length=3, max_length=30)
    estado = forms.CharField(max_length=15)

    def save(self):
        """Crea y guarda un area"""
        data = self.cleaned_data
        area = Area(nombre=data['nombre'], estado=data['estado'],)
        area.save()

class AreaForm(forms.ModelForm):
    """Formulario de Area."""

    class Meta:
        
        model = Area
        fields = ('nombre', 'estado')


#Formularios para Empleado

class FormularioRegistro(forms.Form):

    username = forms.CharField(min_length=4, max_length=50)
    grupo = forms.ChoiceField(choices=GRUPOS)

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
    cargo = forms.CharField(label= 'Cargo')
    tarifa = forms.FloatField(label= 'Tarifa')
    estado = forms.CharField(label= 'Estado')

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use.')
        return username

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
        grupo = Group.objects.filter(pk=data['grupo'])

        if grupo[0].permissions.count() == Permission.objects.count():
            user.is_staff = True
        user.save()

        empleado = Empleado(usuario=user, cedula=data['cedula'], nombre=data['nombre'], 
                            apellido=data['apellido'], direccion=data['direccion'], 
                            fecha_nacimiento=data['fecha_nacimiento'], 
                            cargo=data['cargo'], tarifa=data['tarifa'],
                            estado=data['estado'])
        empleado.save()


class EmpleadoForm(forms.ModelForm):
    """Formulario de Empleado."""

    class Meta:
        
        model = Empleado
        fields = ('cedula','nombre', 'apellido', 'direccion', 'fecha_nacimiento', 'cargo', 'tarifa', 'estado')


#Formularios para Grupos del sistema
class FormCrearGrupo(forms.Form):
    
    nombre = forms.CharField(min_length=3, max_length=30)
    permisos = forms.MultipleChoiceField(choices=CHOICES)


    def save(self):
        """Crea y guarda una factura"""
        data = self.cleaned_data
        grupo = Group.objects.create(name=data['nombre'])
        
        for permission_id in data['permisos']:
            grupo.permissions.add(permission_id)

class GrupoForm(forms.ModelForm):
    class Meta: 
        model = Group
        fields = ('name', 'permissions')


#Formularios para roles
class FormCrearRol(forms.Form):
    
    nombre = forms.CharField(min_length=3, max_length=30)
    tipo = forms.CharField(min_length=4, max_length=20)

    def save(self):
        """Crea y guarda un cliente"""
        data = self.cleaned_data
        rol = Rol(nombre=data['nombre'], tipo=data['tipo'],)
        rol.save()


class RolForm(forms.ModelForm):
    class Meta: 
        model = Rol
        fields = ('nombre', 'tipo')


#Formulario para Servicios
class FormCrearServicio(forms.Form):
    
    detalle = forms.CharField(max_length=30)
    descripcion = forms.CharField(max_length=60)
    estado_final = forms.CharField(max_length=15)
    costo = forms.FloatField()
    area = forms.ModelChoiceField(Area.objects.all())

    def save(self):
        """Crea y guarda un cliente"""
        data = self.cleaned_data
        servicio = Servicio(detalle=data['detalle'], descripcion=data['descripcion'],
                            estado_final=data['estado_final'], costo=data['costo'],
                            area=data['area'],)
        servicio.save()


class ServicioForm(forms.ModelForm):

    class Meta:
        model = Servicio
        fields = ('detalle','descripcion','estado_final','costo','area')