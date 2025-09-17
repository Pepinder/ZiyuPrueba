from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Jardinero(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil_jardinero')
    especialidad = models.CharField(
        max_length=100, blank=True, help_text="Ejemplo: poda, riego, diseño de jardines")

    def __str__(self):
        return self.user.username


class Cliente(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil_cliente')
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username


class SolicitudVisita(models.Model):
    ESTADO_SOLICITADA = 'solicitada'
    ESTADO_ASIGNADA = 'asignada'
    ESTADO_CONFIRMADA = 'confirmada'
    ESTADO_COMPLETADA = 'completada'
    ESTADO_CANCELADA = 'cancelada'

    ESTADOS = [
        (ESTADO_SOLICITADA, 'Solicitada'),
        (ESTADO_ASIGNADA, 'Asignada'),
        (ESTADO_CONFIRMADA, 'Confirmada por Cliente'),
        (ESTADO_COMPLETADA, 'Completada'),
        (ESTADO_CANCELADA, 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='solicitudes')
    jardinero_asignado = models.ForeignKey(
        Jardinero, on_delete=models.SET_NULL, null=True, blank=True, related_name='visitas_asignadas')
    direccion = models.CharField(max_length=300)
    tipo_servicio = models.CharField(max_length=100)
    disponibilidad_horaria = models.CharField(
        max_length=200, help_text="Días y horas disponibles (Jueves y Viernes de 9am a 5pm)")
    metros_cuadrados = models.PositiveIntegerField()
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    estado = models.CharField(
        max_length=20, choices=ESTADOS, default=ESTADO_SOLICITADA)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_visita_confirmada = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Solicitud de {self.cliente.user.username} en {self.direccion}'
