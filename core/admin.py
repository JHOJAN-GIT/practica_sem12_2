from django.contrib import admin
from .models import Equipo, Prestamo
from django.utils import timezone

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('codigo_patrimonial', 'nombre', 'estado', 'laboratorio', 'dias_desde_mantenimiento')
    list_filter = ('estado', 'laboratorio', 'categoria')
    search_fields = ('codigo_patrimonial', 'nombre')
    actions = ['marcar_mantenimiento']

    # Campo calculado
    @admin.display(description='Días desde Mant.')
    def dias_desde_mantenimiento(self, obj):
        if obj.ultimo_mantenimiento:
            return (timezone.now().date() - obj.ultimo_mantenimiento).days
        return "Sin registro"

    # Acción masiva
    @admin.action(description='Marcar seleccionados como En Mantenimiento')
    def marcar_mantenimiento(self, request, queryset):
        queryset.update(estado='mantenimiento')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('docente', 'equipo', 'fecha_prestamo', 'fecha_devolucion', 'estado', 'dias_retraso')
    list_filter = ('estado', 'fecha_prestamo')
    search_fields = ('equipo__codigo_patrimonial', 'docente__username')
    actions = ['enviar_recordatorio']

    @admin.display(description='Días de Retraso')
    def dias_retraso(self, obj):
        if obj.estado == 'activo' and obj.fecha_devolucion < timezone.now().date():
            return (timezone.now().date() - obj.fecha_devolucion).days
        return 0

    @admin.action(description='Enviar recordatorio de devolución')
    def enviar_recordatorio(self, request, queryset):
        # Simulación de envío
        self.message_user(request, f"Recordatorios enviados a {queryset.count()} préstamos.")