from django.shortcuts import render, redirect
from Cooperativa.views import homePage
from .forms import FormularioTransaccion
from django.contrib.auth.decorators import login_required
from app.modelo.models import Transaccion, Cuenta
from django.contrib import messages
import random
# Create your views here.
@login_required
def transaccion(request):
    usuario = request.user
    if usuario.has_perm('modelo.add_transaccion'):
        dni = request.GET['numero']
        c = Cuenta.objects.get(numero=dni)
        trans = Transaccion()
        trans.cuenta = c
        formulario = FormularioTransaccion(instance=trans)

        context = {
            'f': formulario,
            'title': "Transaccion",
            'mensaje': "Ingresar Nueva Transaccion"
        }
        formulario = FormularioTransaccion(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                transaccion = Transaccion()
                transaccion.cuenta = datos.get('cuenta')
                transaccion.tipo = datos.get('tipo')
                transaccion.valor = datos.get('valor')
                transaccion.descripcion = datos.get('descripcion')
                transaccion.cedula_responsable = datos.get('cedula_responsable')
                transaccion.responsable = datos.get('responsable')

                cuenta = Cuenta.objects.get(numero=datos.get('cuenta'))
                if cuenta.estado:
                    cuentaSuma = Cuenta.objects.filter(numero=datos.get('cuenta'))

                    suma = 0
                    for item in cuentaSuma:
                        if datos.get('tipo') == 'deposito':
                            suma = datos.get('valor') + item.saldo
                        if datos.get('tipo') == 'retiro':
                            if item.saldo >= datos.get('valor'):
                                suma = item.saldo - datos.get('valor')
                            else:
                                messages.warning(request, 'SALDO INSUFICIENTE')
                                return render(request, 'transaccion/crear_transaccion.html', context)
                    cuenta.saldo = suma;

                    transaccion.save()
                    cuenta.save()
                    messages.warning(request, 'Guardado Exitosamente')
                    context = {
                        'fecha': transaccion.fecha,
                        'tipo': transaccion.tipo,
                        'valor': transaccion.valor,
                        'cuenta': transaccion.cuenta,
                        'descripcion': transaccion.descripcion,
                        'cedula_responsable': transaccion.cedula_responsable,
                        'responsable': transaccion.responsable
                    }
                    return render(request, 'transaccion/presentar.html', context)
                else:
                    messages.warning(request, 'CUENTA INACTIVA')
                    return redirect(homePage)
        return render(request, 'transaccion/crear_transaccion.html', context)
    else:
        return render(request, 'login/buscar.html')


