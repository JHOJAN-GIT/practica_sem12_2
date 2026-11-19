from django import forms
from django.core.exceptions import ValidationError
from .models import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'fecha_hora', 'motivo']
        widgets = {'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'})}

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if len(motivo) < 20:
            raise ValidationError("El motivo debe tener al menos 20 caracteres.")
        return motivo

    def clean(self):
        cleaned_data = super().clean()
        medico = cleaned_data.get('medico')
        fecha_hora = cleaned_data.get('fecha_hora')
        if medico and fecha_hora:
            if Cita.objects.filter(medico=medico, fecha_hora=fecha_hora, estado='pendiente').exists():
                raise ValidationError("El médico ya tiene una cita en ese horario.")
        return cleaned_data