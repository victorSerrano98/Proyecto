from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse

from .forms import formularioLogin
# Create your views here.


def loginPage (request):
    if request.method =='POST':
        formulario = formularioLogin(request.POST)
        if formulario.is_valid():
            usuario = request.POST['username']
            clave = request.POST['password']
            user = authenticate(username=usuario,password = clave)
            if user is not None: #usuario no es nulo
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('home_page')) #clientes de name de urls de clientes
                    messages.warning(request, 'Te has identificado de forma correcta')
                else:
                    messages.warning(request, 'Usuario inactivo')
            else:
                messages.warning(request,'Usuario y/o contrasena inactivo')
    else:
        formulario = formularioLogin()

    context = {
        'f': formulario,
    }
    return render (request, 'login/login.html', context)

def logoutPage(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))
