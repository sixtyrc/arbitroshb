from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('ARBITRO', 'Árbitro'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='ARBITRO')
    email = models.EmailField(unique=True) # Exigimos email único para Resend

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class Arbitro(models.fields.related.OneToOneField):
    pass # To be defined fully later, but let's just make it a standard Model

class Arbitro(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='perfil_arbitro')
    phone = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.user.get_full_name()

class Partido(models.Model):
    title = models.CharField(max_length=200, help_text="Ej: Final de Chaco - Apertura")
    date_time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.title} - {self.date_time.strftime('%Y-%m-%d %H:%M')}"

class Disponibilidad(models.Model):
    arbitro = models.ForeignKey(Arbitro, on_delete=models.CASCADE, related_name='disponibilidades')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True, help_text="False si reporta inasistencia en este bloque")
    
    def __str__(self):
        estado = "Libre" if self.is_available else "Ocupado"
        return f"{self.arbitro} | {estado} | {self.start_time} - {self.end_time}"

class Designacion(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('ACCEPTED', 'Aceptado'),
        ('REJECTED', 'Rechazado'),
    )
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='designaciones')
    arbitro = models.ForeignKey(Arbitro, on_delete=models.CASCADE, related_name='designaciones')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('partido', 'arbitro')
        
    def __str__(self):
        return f"Designación: {self.arbitro} -> {self.partido.title} ({self.get_status_display()})"
