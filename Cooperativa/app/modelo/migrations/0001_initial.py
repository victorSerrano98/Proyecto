# Generated by Django 2.1.2 on 2019-01-14 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ncuenta', models.CharField(max_length=10)),
                ('Tcuenta', models.CharField(choices=[('a', 'Ahorro'), ('c', 'Credito')], max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('cedula', models.CharField(max_length=10, unique=True)),
                ('nombres', models.CharField(max_length=70)),
                ('apellidos', models.CharField(max_length=70)),
                ('genero', models.CharField(choices=[('femenino', 'Femenino'), ('masculino', 'Masculino')], max_length=15)),
                ('estadoCivil', models.CharField(choices=[('casado', 'Casad@'), ('soltero', 'Solter@'), ('viudo', 'Viud@'), ('divorciado', 'Divorciad@'), ('unionLibre', 'Unión Libre')], max_length=15)),
                ('estado', models.BooleanField()),
                ('fechaNacimiento', models.DateField()),
                ('correo', models.EmailField(max_length=100, unique=True)),
                ('telefono', models.CharField(max_length=15)),
                ('celular', models.CharField(max_length=15)),
                ('direccion', models.TextField()),
                ('cliente_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('cuenta_id', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.CharField(max_length=20, unique=True)),
                ('estado', models.BooleanField()),
                ('fecha_apertura', models.DateField(auto_now=True)),
                ('saldo', models.DecimalField(decimal_places=3, max_digits=10)),
                ('tipo_Cuenta', models.CharField(choices=[('ahorros', 'Ahorro'), ('corriente', 'Corriente')], max_length=30)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelo.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('transaccion_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('retiro', 'Retiro'), ('deposito', 'Deposito')], max_length=10)),
                ('valor', models.DecimalField(decimal_places=3, max_digits=10)),
                ('descripcion', models.TextField()),
                ('cedula_responsable', models.CharField(max_length=10)),
                ('responsable', models.CharField(max_length=300)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modelo.Cuenta')),
            ],
        ),
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('transferencia_id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('valor', models.DecimalField(decimal_places=3, max_digits=10)),
                ('descripcion', models.TextField()),
                ('cuentaDestino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuentaDestino', to='modelo.Cuenta')),
                ('cuentaOrigen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuentaOrigen', to='modelo.Cuenta')),
            ],
        ),
    ]