from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import FormularioCliente
from easygui import boolbox

from app.modelo.models import Cliente,Cuenta #******************CAMBIAR AQUI
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def principal(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cliente'):
        listaClientes = Cliente.objects.filter(estado = True)
        listaClientesInactivos = Cliente.objects.filter(estado=False)

        page = request.GET.get('page', 1)
        paginator = Paginator(listaClientes, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        page = request.GET.get('page', 1)

        paginator = Paginator(listaClientesInactivos, 10)
        try:
            users1 = paginator.page(page)
        except PageNotAnInteger:
            users1 = paginator.page(1)
        except EmptyPage:
            users1 = paginator.page(paginator.num_pages)
        context = {
            'title': "LISTA DE CLIENTES",
            'users' : users,
            'permisoEditar': usuario.has_perm('modelo.change_cliente'),
            'permisoCrear': usuario.has_perm('modelo.add_cliente'),
            'listaInactivos': users1,
        }
        return render(request, 'cliente/principal_cliente.html', context)
    else:
        return render(request, 'login/buscar.html')

def Saludar(request):
    return HttpResponse('BIENVENIDOS')

def crear(request):
    usuario = request.user
    if usuario.has_perm('modelo.add_cliente'):
        formulario = FormularioCliente(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                cliente = Cliente()
                cliente.cedula = datos.get('cedula')
                cliente.nombres = datos.get('nombres')
                cliente.apellidos = datos.get('apellidos')
                cliente.genero = datos.get('genero')
                cliente.estadoCivil = datos.get('estadoCivil')
                cliente.estado= True
                cliente.correo = datos.get('correo')
                cliente.fechaNacimiento = datos.get('fechaNacimiento')
                cliente.telefono = datos.get('telefono')
                cliente.celular = datos.get('celular')
                cliente.direccion = datos.get('direccion')
                cliente.save()
                messages.warning(request, 'Guardado Exitosamente')
                return redirect(principal)
        context = {
            'f': formulario,
            'mensaje': 'Crear nuevo Cliente',
        }
        return render(request, 'cliente/crear_cliente.html', context)
    else:
        return render(request, 'login/buscar.html')


def modificar(request):
    usuario = request.user
    if usuario.has_perm('modelo.change_cliente'):
        dni = request.GET['cedula']
        cliente = Cliente.objects.get(cedula = dni)
        formulario = FormularioCliente(request.POST, instance=cliente)
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                cliente.cedula = datos.get('cedula')
                cliente.nombres = datos.get('nombres')
                cliente.apellidos = datos.get('apellidos')
                cliente.genero = datos.get('genero')
                cliente.estadoCivil = datos.get('estadoCivil')
                cliente.estado = True
                cliente.correo = datos.get('correo')
                cliente.telefono = datos.get('telefono')
                cliente.celular = datos.get('celular')
                cliente.direccion = datos.get('direccion')
                if boolbox(msg='Caja booleana', title='Control: boolbox', choices=('Si(1)', 'No(0)')):
                    cliente.save()
                    messages.warning(request, 'Guardado Exitosamente')
                return redirect(principal)
        else:
            formulario = FormularioCliente(instance=cliente)

        context = {
            'mensaje':'Editar Cliente: '+dni,
            'f': formulario,
        }
        return render(request, 'cliente/crear_cliente.html', context)
    else:
        return render(request, 'login/buscar.html')

def showDialog(request):
    usuario = request.user
    if usuario.has_perm('modelo.delete_cliente'):
        dni = request.GET['cedula']
        cliente = Cliente.objects.get(cedula=dni)
        cliente.estado = False
        if boolbox(msg='¿Desea Eliminar a este usuario?', title='Eliminar', choices=('Si', 'No')):
            cuenta = Cuenta.objects.filter(cliente=cliente)
            for c in cuenta:
                c.estado = False
                c.save()
            cliente.save()
            messages.warning(request, 'Eliminado Exitosamente')
            return redirect(principal)
        else:
            return redirect(principal)
    else:
        return render(request, 'login/buscar.html')

def ActivarCliente(request):
    usuario = request.user
    if usuario.has_perm('modelo.delete_cliente'):
        dni = request.GET['cedula']
        cliente = Cliente.objects.get(cedula=dni)
        cliente.estado = True
        if boolbox(msg='¿Desea Activar a este usuario?', title='Activar Cliente', choices=('Si', 'No')):
            cuenta = Cuenta.objects.filter(cliente=cliente)
            for c in cuenta:
                c.estado = True
                c.save()
            cliente.save()
            messages.warning(request, 'Activado Exitosamente')
            return redirect(principal)
        else:
            return redirect(principal)
    else:
        return render(request, 'login/buscar.html')


@login_required()
def buscar(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cliente'):
        dni = request.GET['txt_buscar']
        lista = Cliente.objects.filter(cedula=dni)

        listaClientes = lista.filter(estado=True)
        listaClientesInactivos = lista.filter(estado=False)

        page = request.GET.get('page', 1)
        paginator = Paginator(listaClientes, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        page = request.GET.get('page', 1)

        paginator = Paginator(listaClientesInactivos, 10)
        try:
            users1 = paginator.page(page)
        except PageNotAnInteger:
            users1 = paginator.page(1)
        except EmptyPage:
            users1 = paginator.page(paginator.num_pages)
        context = {
            'title': "LISTA DE CLIENTES",
            'users': users,
            'permisoEditar': usuario.has_perm('modelo.change_cliente'),
            'permisoCrear': usuario.has_perm('modelo.add_cliente'),
            'listaInactivos': users1,

        }
        return render(request, 'cliente/principal_cliente.html', context)
    else:
        return render(request, 'login/buscar.html')

@login_required()
def verCuentas(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cuenta'):
        dni = request.GET['cedula']
        c = Cliente.objects.get(cedula = dni)
        listaClientes = Cuenta.objects.filter(cliente = c).order_by('cuenta_id')
        lista = listaClientes.filter(estado=True)
        listaInactivos = listaClientes.filter(estado=False)

        page = request.GET.get('page', 1)
        paginator = Paginator(lista, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        page = request.GET.get('page', 1)
        paginator = Paginator(listaInactivos, 10)
        try:
            users1 = paginator.page(page)
        except PageNotAnInteger:
            users1 = paginator.page(1)
        except EmptyPage:
            users1 = paginator.page(paginator.num_pages)

        context = {
            'title': "LISTA DE CUENTAS",
            'cedula': dni,
            'cliente': c,
            'listaInactivos' : users1,
            'users': users,
            'permisoCrear': usuario.has_perm('modelo.add_cuenta'),
            'permisoEditar': usuario.has_perm('modelo.change_cuenta'),
        }
        return render(request, 'cliente/verCuentas.html', context,)
    else:
        return render(request, 'login/buscar.html')


def master(request):
    return render(request, 'master.html')

