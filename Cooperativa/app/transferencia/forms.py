from django import forms
from app.modelo.models import Transferencia

class FormularioTransferencia(forms.ModelForm):
    class Meta:
        model = Transferencia
        fields = ["cuentaOrigen", "cuentaDestino", "valor", "descripcion"]

