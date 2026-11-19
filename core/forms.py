import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Prestamo, Equipo

# ==========================================
# 1. MODELFORM (Rúbrica: Formulario atado a modelo)
# ==========================================
class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['equipo', 'fecha_devolucion', 'cantidad', 'observaciones']
        widgets = {
            'fecha_devolucion': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones adicionales...'}),
        }

    # Recibimos el usuario desde la vista para la validación cruzada
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    # Validación por campo (clean_<campo>)
    def clean_fecha_devolucion(self):
        fecha_dev = self.cleaned_data.get('fecha_devolucion')
        if fecha_dev and fecha_dev <= timezone.now().date():
            raise ValidationError("La fecha de devolución debe ser posterior a hoy.")
        return fecha_dev

    # Validación de campo con Regex y Sanitización
    def clean_observaciones(self):
        obs = self.cleaned_data.get('observaciones')
        if obs:
            # Sanitización básica (quitar espacios extra)
            obs = obs.strip()
            # Evitar inyección de scripts básica (Regex)
            if re.search(r'<script.*?>.*?</script>', obs, re.IGNORECASE):
                raise ValidationError("Las observaciones contienen caracteres no permitidos.")
            if len(obs) < 5:
                raise ValidationError("La observación debe tener al menos 5 caracteres.")
        return obs

    # Validación cruzada (clean)
    def clean(self):
        cleaned_data = super().clean()
        equipo = cleaned_data.get('equipo')
        cantidad = cleaned_data.get('cantidad')

        # 1. Validar estado del equipo
        if equipo and equipo.estado != 'operativo':
            self.add_error('equipo', 'El equipo seleccionado no está operativo (está en mantenimiento o de baja).')

        # 2. Validar límite de 3 préstamos activos por docente
        if self.user:
            prestamos_activos = Prestamo.objects.filter(docente=self.user, estado='activo').count()
            # Si estamos editando, restamos 1 si el préstamo actual ya estaba activo
            if self.instance.pk and self.instance.estado == 'activo':
                prestamos_activos -= 1
            
            if prestamos_activos >= 3:
                raise ValidationError("Límite alcanzado: El docente no puede tener más de 3 préstamos activos simultáneamente.")

        return cleaned_data


# ==========================================
# 2. FORMULARIO CLÁSICO (Rúbrica: ModelForm + clásico)
# ==========================================
class BusquedaEquipoForm(forms.Form):
    termino = forms.CharField(
        max_length=50, 
        label="Buscar equipo por nombre o código",
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Laptop HP o EQ-001'})
    )
    
    def clean_termino(self):
        termino = self.cleaned_data.get('termino')
        if len(termino) < 3:
            raise ValidationError("Ingresa al menos 3 caracteres para realizar la búsqueda.")
        return termino