from django.shortcuts import render, redirect
from django.contrib import messages
from Cooperativa.views import homePage
from django.contrib.auth.decorators import login_required
from .forms import FormularioTransferencia
from app.modelo.models import Transferencia, Cuenta
# Create your views here.
@login_required
def crearTransferencia(request):
    usuario = request.user
    if usuario.has_perm('modelo.add_transferencia'):
        dni = request.GET['numero']
        c = Cuenta.objects.get(numero=dni)
        trans = Transferencia()
        trans.cuentaOrigen = c
        formulario = FormularioTransferencia(instance=trans)


        context = {
            'f': formulario,
            'title': "Ingresar Cliente",
            'mensaje': "Ingresar Nuevo Cliente"
        }
        formulario = FormularioTransferencia(request.POST)
        if request.method == 'POST':
            if formulario.is_valid():
                datos = formulario.cleaned_data
                transferencia = Transferencia()
                transferencia.cuentaOrigen = datos.get('cuentaOrigen')
                transferencia.cuentaDestino = datos.get('cuentaDestino')
                transferencia.valor = datos.get('valor')
                transferencia.descripcion = datos.get('descripcion')

                cuenta1 = Cuenta.objects.get(numero=datos.get('cuentaOrigen'))
                cuenta2 = Cuenta.objects.get(numero=datos.get('cuentaDestino'))
                if cuenta2.estado & cuenta1.estado:
                    cuentaSuma = Cuenta.objects.filter(numero=datos.get('cuentaOrigen'))
                    suma = 0
                    for item in cuentaSuma:
                        if item.saldo >= datos.get('valor'):
                            suma = item.saldo - datos.get('valor')
                        else:
                            messages.warning(request, 'SALDO INSUFICIENTE')
                            return render(request, 'clientes/Transaccion.html', context)
                    cuenta1.saldo = suma;


                    cuentaSuma2 = Cuenta.objects.filter(numero=datos.get('cuentaDestino'))
                    for item in cuentaSuma2:
                        suma = item.saldo + datos.get('valor')
                    cuenta2.saldo = suma;

                    transferencia.save()
                    cuenta1.save()
                    cuenta2.save()
                    messages.warning(request, 'Guardado Exitosamente')
                    context = {
                        'fecha': transferencia.fecha,
                        'valor': transferencia.valor,
                        'cuentaOrigen': transferencia.cuentaOrigen,
                        'cuentaDestino': transferencia.cuentaDestino,
                        'descripcion': transferencia.descripcion
                    }
                    return render(request, 'transferencia/presentar_transferencia.html', context)

                else:
                    messages.warning(request, 'CUENTA DE DESTINO INACTIVA')
                    return redirect(homePage)
        return render(request, 'transferencia/crear_transferencia.html', context)
    else:
        return render(request, 'login/buscar.html')
