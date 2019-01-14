from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponse
from easygui import boolbox

from .forms import FormularioCuenta
from django.contrib import messages
from app.modelo.models import Cuenta, Transaccion, Transferencia, Cliente
import random
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required()
def principal(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cuenta'):
        listaCuentas = Cuenta.objects.filter(estado = True)
        listaCuentasInactivas = Cuenta.objects.filter(estado=False)

        page = request.GET.get('page', 1)
        paginator = Paginator(listaCuentas, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        page1 = request.GET.get('page', 1)
        paginator = Paginator(listaCuentasInactivas, 10)
        try:
            users1 = paginator.page(page)
        except PageNotAnInteger:
            users1 = paginator.page(1)
        except EmptyPage:
            users1 = paginator.page(paginator.num_pages)
        context = {
            'title': "LISTA DE CUENTAS",
            'users': users,
            'permisoEditar': usuario.has_perm('modelo.change_cuenta'),
            'permisoCrear': usuario.has_perm('modelo.add_cuenta'),
            'listaInactivas': users1,
        }
        return render(request, 'cuenta/principal_cuenta.html', context)
    else:
        return render(request, 'login/buscar.html')


@login_required
def crearCuentaCliente(request):
        usuario = request.user
        if usuario.has_perm('modelo.add_cuenta'):
            dni = request.GET['cedula']
            c = Cliente.objects.get(cedula=dni)
            client = Cuenta()
            client.cliente = c
            formulario = FormularioCuenta(instance=client)
            numero = random.randint(1000000000, 9999999999)
            context = {
                'f': formulario,
                'title': "Ingresar Cliente",
                'numero': numero,
                'mensaje': "Ingresar Nueva Cuenta"
            }
            formulario = FormularioCuenta(request.POST)
            num = numero.__str__()
            while Cuenta.objects.filter(numero=num).exists():
                numero = random.randrange(10)
            if request.method == 'POST':
                if formulario.is_valid():
                    datos = formulario.cleaned_data
                    cuenta = Cuenta()
                    cuenta.numero = num
                    cuenta.saldo = "0"
                    cuenta.estado=True
                    cuenta.cliente = datos.get('cliente')
                    cuenta.tipo_Cuenta = datos.get('tipo_Cuenta')
                    cuenta.save()
                    messages.warning(request, 'Guardado Exitosamente')
                    return redirect(principal)

            return render(request, 'cuenta/crear_cuenta.html', context)
        else:
            return render(request, 'login/buscar.html')


@login_required()
def buscar(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_cuenta'):
        dni = request.GET['txt_buscar']
        lista = Cuenta.objects.filter(numero=dni)

        listaCuentas = lista.filter(estado=True)
        listaCuentasInactivas = lista.filter(estado=False)

        page = request.GET.get('page', 1)
        paginator = Paginator(listaCuentas, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        page1 = request.GET.get('page', 1)
        paginator = Paginator(listaCuentasInactivas, 10)
        try:
            users1 = paginator.page(page)
        except PageNotAnInteger:
            users1 = paginator.page(1)
        except EmptyPage:
            users1 = paginator.page(paginator.num_pages)
        context = {
            'title': "LISTA DE CUENTAS",
            'users': users,
            'listaInactivas': users1,
            'permisoEditar': usuario.has_perm('modelo.change_cuenta'),
            'permisoCrear': usuario.has_perm('modelo.add_cuenta'),
        }
        return render(request, 'cuenta/principal_cuenta.html', context)
    else:
        return redirect(principal)

def modificar(request):
    usuario = request.user
    if usuario.has_perm('modelo.change_cuenta'):
        dni = request.GET['numero']
        cuenta = Cuenta.objects.get(numero = dni)
        formulario = FormularioCuenta(request.POST, instance=cuenta)
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                cuenta.saldo = cuenta.saldo
                cuenta.cliente = datos.get('cliente')
                cuenta.tipo_Cuenta = datos.get('tipo_Cuenta')
                cuenta.save()
                messages.warning(request, 'Guardado Exitosamente')
                if boolbox(msg='Deser Modificar la cuenta: '+dni, title='Control: boolbox', choices=('Si', 'No')):
                    cuenta.save()
                    messages.warning(request, 'Guardado Exitosamente')
                return redirect(principal)
        else:
            formulario = FormularioCuenta(instance=cuenta)

        context = {
            'title': "Modificar Cuenta: "+dni,
            'f': formulario,
        }
        return render(request, 'cliente/crear_cliente.html', context)
    else:
        messages.warning(request, 'No Permitido')
        return render(request, 'login/buscar.html')

def showDialog(request):
    usuario = request.user
    if usuario.has_perm('modelo.delete_cliente'):
        dni = request.GET['numero']
        cliente = Cuenta.objects.get(numero=dni)
        cliente.estado = False
        if boolbox(msg='¿Desea Eliminar la cuenta: '+ dni, title='ELIMINAR', choices=('Si', 'No')):
            cliente.save()
            messages.warning(request, 'Eliminado Exitosamente')
            return redirect(principal)
        else:
            return redirect(principal)
    else:
        return render(request, 'login/buscar.html')


def ActivarCuenta(request):
    usuario = request.user
    if usuario.has_perm('modelo.delete_cliente'):
        dni = request.GET['numero']
        cliente = Cuenta.objects.get(numero=dni)
        c = Cliente.objects.get(cedula=cliente.cliente)
        if c.estado:
            cliente.estado = True
            if boolbox(msg='¿Desea Activar la Cuenta: ' + dni, title='Activar', choices=('Si', 'No')):
                cliente.save()
                messages.warning(request, 'Activado Exitosamente')
                return redirect(principal)
            else:
                return redirect(principal)
        else:
            messages.warning(request, 'CLIENTE INACTIVO')
            return redirect(principal)

    else:
        return render(request, 'login/buscar.html')


@login_required()
def verTransaccion(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_transaccion'):
        dni = request.GET['numero']
        c = Cuenta.objects.get(numero = dni)
        cliente = Cliente.objects.get(cedula=c.cliente)
        listaClientesTransaccion = Transaccion.objects.filter(cuenta = c)
        listaClientesTransferencia = Transferencia.objects.filter(cuentaOrigen=c)
        listaClientesTransferencia1 = Transferencia.objects.filter(cuentaDestino=c)

        page = request.GET.get('page', 1)
        paginator = Paginator(listaClientesTransaccion, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        page = request.GET.get('page', 1)
        paginator1 = Paginator(listaClientesTransferencia, 10)
        try:
            users1 = paginator1.page(page)
        except PageNotAnInteger:
            users1 = paginator1.page(1)
        except EmptyPage:
            users1 = paginator1.page(paginator1.num_pages)

        page = request.GET.get('page', 1)
        paginator1 = Paginator(listaClientesTransferencia1, 10)
        try:
            users2 = paginator1.page(page)
        except PageNotAnInteger:
            users2 = paginator1.page(1)
        except EmptyPage:
            users2 = paginator1.page(paginator1.num_pages)

        context = {
            'title': "LISTA DE TRANSACCIONES DE: "+dni,
            'title1': "LISTA DE TRANSFERENCIAS DE: "+ dni,
            'numero': dni,
            'cuenta': c,
            'cliente': cliente,
            'users' : users,
            'lista1': users1,
            'lista2': users2,
            'permisoCrearTransaccion': usuario.has_perm('modelo.add_transaccion'),
            'permisoCrearTransferencia': usuario.has_perm('modelo.add_transferencia'),

        }
        return render(request, 'transaccion/verTransacciones.html', context)
    else:
        return render(request, 'login/buscar.html')

def imprimir(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_transaccion'):
        id = request.GET['id']
        c = Transaccion.objects.get(transaccion_id=id)
        context = {
            'fecha': c.fecha,
            'tipo': c.tipo,
            'valor': c.valor,
            'cuenta': c.cuenta,
            'descripcion': c.descripcion,
            'cedula_responsable': c.cedula_responsable,
            'responsable': c.responsable
        }
        return render(request, 'transaccion/presentar.html', context)
    else:
        return render(request, 'login/buscar.html')


def imprimirTransferencia(request):
    usuario = request.user
    if usuario.has_perm('modelo.view_transferencia'):
        id = request.GET['id']
        c = Transferencia.objects.get(transferencia_id=id)
        context = {
            'cuentaOrigen': c.cuentaOrigen,
            'cuentaDestino': c.cuentaDestino,
            'valor': c.valor,
            'fecha': c.fecha,
            'descripcion': c.descripcion,
        }
        return render(request, 'transferencia/presentar_transferencia.html', context)
    else:
        return render(request, 'login/buscar.html')

