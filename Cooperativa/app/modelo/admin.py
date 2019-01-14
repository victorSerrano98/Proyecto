from builtins import list

from django.contrib import admin

# Register your models here.
from .models import Cliente
from .models import Banco
from .models import Cuenta
from .models import Transaccion
from .models import Transferencia

class AdminCliente(admin.ModelAdmin):
    list_display = ["cliente_id", "cedula", "apellidos", "nombres", "genero", "estadoCivil","estado", "fechaNacimiento", "correo", "telefono", "direccion","celular"]
    list_editable = ["cedula", "apellidos", "nombres","estado"]
    list_filter = ["genero", "estadoCivil"]
    search_fields = ["cedula"]

    class Meta:
        model = Cliente

admin.site.register(Cliente, AdminCliente)

class AdminBanco(admin.ModelAdmin):
    list_display = ["Ncuenta","Tcuenta"]
    search_fields = ["Ncuenta"]

    class Meta:
        model = Banco

admin.site.register(Banco, AdminBanco)

class AdminCuenta(admin.ModelAdmin):
    list_display = ["cuenta_id", "numero", "estado", "fecha_apertura", "saldo", "tipo_Cuenta", "cliente"]
    list_editable = ["estado", "tipo_Cuenta"]
    search_fields = ["numero"]
    list_filter = ["tipo_Cuenta"]
    class Meta:
        model = Cuenta

admin.site.register(Cuenta, AdminCuenta)

class AdminTransaccion(admin.ModelAdmin):
    list_display = ["transaccion_id", "fecha", "tipo", "valor", "descripcion", "responsable", 'cuenta']
    search_fields = ["transaccion_id"]
    list_filter = ["tipo"]

    class Meta:
        model = Transaccion

admin.site.register(Transaccion, AdminTransaccion)

class AdminTransferencia(admin.ModelAdmin):

    list_display = ["transferencia_id","fecha", "valor", "descripcion", "cuentaOrigen", "cuentaDestino"]
    search_fields = ["cuentaOrigen","cuentaDestino" "descripcion"]

    class Meta:
        model = Transferencia

admin.site.register(Transferencia, AdminTransferencia)