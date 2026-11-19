from django import forms
from django.core.exceptions import ValidationError
from .models import Permiso, Asistencia
from django.utils import timezone

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ['tipo', 'fecha_inicio', 'fecha_fin', 'motivo']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if len(motivo) < 30:
            raise ValidationError("El motivo debe tener al menos 30 caracteres.")
        return motivo

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('fecha_inicio')
        fin = cleaned_data.get('fecha_fin')
        if inicio and fin and fin < inicio:
            raise ValidationError("La fecha de fin no puede ser anterior a la fecha de inicio.")
        return cleaned_data

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = [] # Solo botones, no campos manuales