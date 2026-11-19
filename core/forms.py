from django import forms
from django.core.exceptions import ValidationError
from .models import Prestamo, Equipo
from django.utils import timezone

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['equipo', 'fecha_devolucion', 'cantidad', 'observaciones']
        widgets = {
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }

    # Validación por campo (clean_<campo>)
    def clean_fecha_devolucion(self):
        fecha_dev = self.cleaned_data.get('fecha_devolucion')
        if fecha_dev and fecha_dev <= timezone.now().date():
            raise ValidationError("La fecha de devolución debe ser posterior a hoy.")
        return fecha_dev

    def clean_observaciones(self):
        obs = self.cleaned_data.get('observaciones')
        # Sanitización básica
        if obs:
            return obs.strip()
        return obs

    # Validación cruzada (clean)
    def clean(self):
        cleaned_data = super().clean()
        equipo = cleaned_data.get('equipo')
        cantidad = cleaned_data.get('cantidad')
        docente = self.instance.docente if self.instance.pk else None

        # Validar estado del equipo
        if equipo and equipo.estado != 'operativo':
            self.add_error('equipo', 'El equipo seleccionado no está operativo.')

        # Validar límite de 3 préstamos activos
        if docente:
            prestamos_activos = Prestamo.objects.filter(docente=docente, estado='activo').count()
            # Si estamos editando, restamos 1 si el préstamo actual ya estaba activo
            if self.instance.pk and self.instance.estado == 'activo':
                prestamos_activos -= 1
            
            if prestamos_activos >= 3:
                raise ValidationError("El docente no puede tener más de 3 préstamos activos simultáneamente.")

        return cleaned_data