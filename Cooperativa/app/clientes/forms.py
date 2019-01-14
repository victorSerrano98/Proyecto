from django import forms
from app.modelo.models import Cliente #******************CAMBIAR AQUI

class FormularioCliente(forms.ModelForm):
    class Meta:
        model= Cliente
        fields = ["cedula", "apellidos", "nombres", "genero", "estadoCivil", "fechaNacimiento", "correo", "telefono", "celular", "direccion"]
class FormularioBuscar(forms.ModelForm):

    campo_rechazo = forms.CharField(widget=forms.Textarea(attrs={'cols': 58, 'rows': 9}))