from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Equipo(models.Model):
    ESTADOS = [
        ('operativo', 'Operativo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('baja', 'Dado de Baja'),
    ]
    codigo_patrimonial = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='operativo')
    laboratorio = models.CharField(max_length=50)
    ultimo_mantenimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo_patrimonial} - {self.nombre}"

class Prestamo(models.Model):
    ESTADOS_PRESTAMO = [
        ('activo', 'Activo'),
        ('devuelto', 'Devuelto'),
        ('retrasado', 'Retrasado'),
    ]
    docente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestamos')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField()
    cantidad = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADOS_PRESTAMO, default='activo')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Préstamo de {self.equipo.nombre} a {self.docente.username}"