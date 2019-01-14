from os import name

from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name = 'clientes'),
    #    controller -- metodo
    path('primermensaje', views.Saludar),
    path('crear', views.crear),
    path('modificar', views.modificar),
    path('showDialog', views.showDialog),
    path('ActivarCliente', views.ActivarCliente),
    path('master', views.master),
    path('buscar', views.buscar),
    path('presentarCuentas', views.verCuentas)
]