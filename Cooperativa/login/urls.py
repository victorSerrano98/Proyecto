from django.urls import path

from . import views

urlpatterns= [
    path('', views.loginPage, name= 'autentificar'),
    path('logout', views.logoutPage, name= 'logout'),
]