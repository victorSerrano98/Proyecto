from django.db import models

# Create your models here.
class Cliente(models.Model):

    listaGenero = (
        ('femenino', 'Femenino'),
        ('masculino', 'Masculino'),
    )
    listaEstadoCivil = (
        ('casado', 'Casad@'),
        ('soltero', 'Solter@'),
        ('viudo', 'Viud@'),
        ('divorciado', 'Divorciad@'),
        ('unionLibre', 'Unión Libre'),
    )
    cedula=models.CharField(max_length = 10, unique= True, null=False)
    nombres=models.CharField(max_length = 70, null=False,)
    apellidos=models.CharField(max_length = 70, null=False,)
    genero=models.CharField(max_length = 15, choices = listaGenero, null=False,)
    estadoCivil=models.CharField(max_length = 15, choices = listaEstadoCivil, null=False,)
    estado = models.BooleanField(null=False)
    fechaNacimiento=models.DateField( null= False,)
    correo=models.EmailField(max_length = 100, unique=True, null= False,)
    telefono=models.CharField(max_length = 15,)
    celular=models.CharField(max_length = 15, null = False,)
    direccion=models.TextField(null=False,)
    cliente_id=models.AutoField( primary_key = True,)
    def __str__(self):
        return self.cedula

class Cuenta(models.Model):

    tipoCuenta = (
        ('ahorros', 'Ahorro'),
        ('corriente', 'Corriente'),
    )

    cuenta_id=models.AutoField(primary_key = True,)
    numero=models.CharField(max_length = 20, unique = True)
    estado = models.BooleanField(null=False)
    fecha_apertura = models.DateField(auto_now = True,)
    saldo= models.DecimalField(max_digits = 10, decimal_places = 3 ,)
    tipo_Cuenta=models.CharField(max_length = 30, choices = tipoCuenta, null = False,)
    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.numero

class Transaccion(models.Model):

    listaTransaccion = (
        ('retiro', 'Retiro'),
        ('deposito', 'Deposito'),
    )
    transaccion_id=models.AutoField(primary_key=True)
    fecha=models.DateTimeField(auto_now_add=True)
    tipo=models.CharField(choices=listaTransaccion,max_length=10)
    valor=models.DecimalField(max_digits=10, decimal_places=3,)
    descripcion=models.TextField()
    cedula_responsable = models.CharField(max_length=10, null=False)
    responsable=models.CharField(max_length = 300, null=False)
    cuenta = models.ForeignKey(
        'Cuenta',
        on_delete=models.CASCADE,
    )


class Transferencia(models.Model):

    transferencia_id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add = True, null = False)
    valor = models.DecimalField(max_digits=10, decimal_places=3, null = False)
    descripcion = models.TextField(null = False)
    cuentaOrigen = models.ForeignKey(
        'Cuenta',
            related_name='cuentaOrigen',
        on_delete=models.CASCADE,
    )
    cuentaDestino = models.ForeignKey(
        'Cuenta',
        related_name='cuentaDestino',
        on_delete=models.CASCADE,
    )



class Banco(models.Model):

    tipoCuenta = (
        ('a', 'Ahorro'),
        ('c', 'Credito'),
    )

    Ncuenta=models.CharField(max_length = 10)
    Tcuenta=models.CharField(max_length = 25, choices = tipoCuenta, null = True)