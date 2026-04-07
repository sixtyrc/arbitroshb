import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

# Configuración de rutas para encontrar el proyecto
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from gestion.models import CustomUser, Arbitro, Partido

def seed():
    # 1. Crear Superusuario (Admin)
    if not CustomUser.objects.filter(username='admin').exists():
        admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@ctsoft.com.ar',
            password='admin',
            role='ADMIN',
            first_name='Admin',
            last_name='General'
        )
        print("Superusuario 'admin' creado (pass: admin)")
    else:
        print("Superusuario 'admin' ya existe")

    # 2. Crear Árbitro de prueba
    if not CustomUser.objects.filter(username='arbitro1').exists():
        u1 = CustomUser.objects.create_user(
            username='arbitro1',
            email='arbitro1@test.com',
            password='arbitro123',
            role='ARBITRO',
            first_name='Juan',
            last_name='Pérez'
        )
        Arbitro.objects.create(user=u1, phone='3624123456', category='Nacional')
        print("Árbitro 'arbitro1' creado (pass: arbitro123)")

    # 3. Crear Partidos
    if not Partido.objects.exists():
        Partido.objects.create(
            title='Final Masculina - Chaco vs Corrientes',
            date_time=timezone.now() + timedelta(days=2),
            location='Microestadio Sarmiento'
        )
        Partido.objects.create(
            title='Semifinal Femenina - Apertura',
            date_time=timezone.now() + timedelta(days=3),
            location='Club San Martín'
        )
        print("Partidos de prueba creados.")

if __name__ == "__main__":
    seed()
