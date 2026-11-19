from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Area(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.nombre

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8, unique=True)
    cargo = models.CharField(max_length=50, default='Empleado')
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    fecha_ingreso = models.DateField(default=timezone.now)
    def __str__(self): return f"{self.user.username} - {self.area}"

class Asistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_salida = models.DateTimeField(null=True, blank=True)
    def __str__(self): return f"Asistencia {self.empleado.user.username} - {self.fecha}"

class Permiso(models.Model):
    ESTADOS = [('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')]
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    def __str__(self): return f"Permiso {self.empleado.user.username} - {self.estado}"