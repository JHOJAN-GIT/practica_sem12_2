from django.db import models
from django.contrib.auth.models import User

class Paciente(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    alergias = models.TextField(blank=True)

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cmp = models.CharField(max_length=10, unique=True)
    especialidad = models.CharField(max_length=50)

class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, default='pendiente')