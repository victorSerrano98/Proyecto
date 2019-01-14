from django import forms
from app.modelo.models import Transaccion

class FormularioTransaccion(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ["cuenta", "tipo", "valor", "descripcion", "cedula_responsable", "responsable"]