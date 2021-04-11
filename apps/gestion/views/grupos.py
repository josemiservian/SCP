# Django
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, Permission

#Decoradores
from scp.decorators import allowed_users

#Formularios
from apps.gestion.forms import FormCrearGrupo, GrupoForm

#FUNCIONES
@login_required(login_url='empleados/login')
@allowed_users(action='add_group')
def crear_grupo(request):

	form = FormCrearGrupo()

	if request.method == 'POST':
		form = FormCrearGrupo(request.POST)
		if form.is_valid():
			form.save()
			return redirect('gestion:grupos-listar')

	context = {'form':form}
	return render(request, 'grupos/crear.html', context)

@login_required(login_url='empleados/login')
@allowed_users(action='view_group')
def listar_grupos(request):

    grupos = Group.objects.all()
    return render(request, 'grupos/listar.html', {'grupos':grupos})

@login_required(login_url='empleados/login')
@allowed_users(action='change_group')
def actualizar_grupo(request, pk):

	grupo = Group.objects.get(id=pk)
	form = GrupoForm(instance=grupo)

	if request.method == 'POST':
		form = GrupoForm(request.POST, instance=grupo)
		if form.is_valid():
			form.save()
			return redirect('gestion:grupos-listar')

	context = {'form':form}
	return render(request, 'grupos/modificar.html', context)


@login_required(login_url='empleados/login')
@allowed_users(action='delete_group')
def borrar_grupo(request, pk):
	
    grupo = Group.objects.get(id=pk)
    if request.method == "POST":
        grupo.delete()
        return redirect('gestion:grupos-listar')
        
    context = {'grupo':grupo}
    return render(request, 'grupos/borrar.html', context)

@login_required(login_url='empleados/login')
@allowed_users(action='delete_group')
def selector(request):
	
	form = FormCrearGrupo()

	if request.method == 'POST':
		form = FormCrearGrupo(request.POST)
		if form.is_valid():
			form.save()
			return redirect('gestion:grupos-listar')

	context = {'form':form}
	return render(request, 'grupos/selector2.html', context)