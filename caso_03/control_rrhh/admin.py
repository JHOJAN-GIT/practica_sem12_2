from django.contrib import admin
from .models import Empleado, Asistencia, Permiso, Area

@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'tipo', 'fecha_inicio', 'fecha_fin', 'estado', 'dias_solicitados')
    list_filter = ('estado', 'tipo', 'empleado__area')
    search_fields = ('empleado__dni', 'empleado__user__username')
    actions = ['aprobar_permisos']

    @admin.display(description='Días Solicitados')
    def dias_solicitados(self, obj):
        return (obj.fecha_fin - obj.fecha_inicio).days + 1

    @admin.action(description='Aprobar permisos seleccionados')
    def aprobar_permisos(self, request, queryset):
        queryset.update(estado='aprobado')

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'fecha', 'hora_entrada', 'hora_salida', 'horas_trabajadas')
    list_filter = ('fecha', 'empleado__area')

    @admin.display(description='Horas Trabajadas')
    def horas_trabajadas(self, obj):
        if obj.hora_entrada and obj.hora_salida:
            delta = obj.hora_salida - obj.hora_entrada
            return round(delta.total_seconds() / 3600, 2)
        return "Pendiente"

admin.site.register(Empleado)
admin.site.register(Area)