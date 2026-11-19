from django.contrib import admin
from .models import Paciente, Medico, Cita
from django.utils import timezone

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'medico', 'fecha_hora', 'estado', 'edad_paciente')
    list_filter = ('estado', 'fecha_hora', 'medico__especialidad')
    search_fields = ('paciente__dni', 'paciente__nombres')
    actions = ['marcar_completadas']

    @admin.display(description='Edad Paciente')
    def edad_paciente(self, obj):
        return (timezone.now().date() - obj.paciente.fecha_nacimiento).days // 365

    @admin.action(description='Marcar seleccionadas como Completadas')
    def marcar_completadas(self, request, queryset):
        queryset.update(estado='completada')

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombres', 'fecha_nacimiento')
    search_fields = ('dni', 'nombres')