from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('ARBITRO', 'Árbitro'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='ARBITRO')
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

class CategoriaGrupo(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    grupo = models.ForeignKey(CategoriaGrupo, on_delete=models.SET_NULL, null=True, blank=True, related_name='categorias')
    def __str__(self):
        return self.nombre

class Arancel(models.Model):
    ROLE_TYPE = (
        ('ARBITRO', 'Árbitro'),
        ('MESA', 'Mesa de Control'),
    )
    rol = models.CharField(max_length=20, choices=ROLE_TYPE)
    categoria_grupo = models.ForeignKey(CategoriaGrupo, on_delete=models.CASCADE, related_name='aranceles')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        unique_together = ('rol', 'categoria_grupo')
    def __str__(self):
        return f"{self.get_rol_display()} - {self.categoria_grupo.nombre}: ${self.monto}"

class Arbitro(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='perfil_arbitro')
    phone = models.CharField(max_length=20, blank=True, null=True)
    cbu_alias = models.CharField(max_length=100, blank=True, null=True, verbose_name="CBU / Alias")
    categoria_max = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.get_full_name()

class Partido(models.Model):
    title = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='partidos', null=True)
    date_time = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.title} ({self.categoria.nombre if self.categoria else 'S/C'})"

class Disponibilidad(models.Model):
    arbitro = models.ForeignKey(Arbitro, on_delete=models.CASCADE, related_name='disponibilidades')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.arbitro} | {'Libre' if self.is_available else 'Ocupado'}"

class Designacion(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pendiente'),
        ('ACCEPTED', 'Aceptado'),
        ('REJECTED', 'Rechazado'),
    )
    ROLE_IN_MATCH = (
        ('ARBITRO_1', 'Árbitro 1'),
        ('ARBITRO_2', 'Árbitro 2'),
        ('MESA', 'Mesa de Control'),
    )
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='designaciones')
    arbitro = models.ForeignKey(Arbitro, on_delete=models.CASCADE, related_name='designaciones')
    rol_asignado = models.CharField(max_length=20, choices=ROLE_IN_MATCH, default='ARBITRO_1')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('partido', 'arbitro')
        
    def __str__(self):
        return f"{self.arbitro} como {self.get_rol_asignado_display()} en {self.partido.title}"

    @property
    def monto_honorario(self):
        if not self.partido.categoria or not self.partido.categoria.grupo:
            return 0
        tipo_arancel = 'MESA' if self.rol_asignado == 'MESA' else 'ARBITRO'
        arancel = Arancel.objects.filter(categoria_grupo=self.partido.categoria.grupo, rol=tipo_arancel).first()
        return arancel.monto if arancel else 0


class PushSubscription(models.Model):
    """Almacena las suscripciones Web Push de cada árbitro."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='push_subscription')
    endpoint = models.TextField()
    p256dh = models.TextField()
    auth = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Push sub de {self.user.username}"
