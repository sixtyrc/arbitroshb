from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ArbitroViewSet, PartidoViewSet, DisponibilidadViewSet, DesignacionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'arbitros', ArbitroViewSet)
router.register(r'partidos', PartidoViewSet)
router.register(r'disponibilidades', DisponibilidadViewSet)
router.register(r'designaciones', DesignacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
