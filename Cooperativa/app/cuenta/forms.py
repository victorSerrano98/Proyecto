from django import forms
from app.modelo.models import Cuenta #******************CAMBIAR AQUI

class FormularioCuenta(forms.ModelForm):
    class Meta:
        model= Cuenta
        fields = ["cliente", "tipo_Cuenta"]
