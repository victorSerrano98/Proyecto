from os import name

from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name = 'cuentas'),
    path('crearCuentaCliente', views.crearCuentaCliente),
    path('buscar', views.buscar),
    path('ActivarCuenta', views.ActivarCuenta),
    path('modificar', views.modificar),
    path('showDialog', views.showDialog),
    path('verTransaccion',views.verTransaccion),
    path('imprimir', views.imprimir),
    path('imprimirTransferencia', views.imprimirTransferencia),
]