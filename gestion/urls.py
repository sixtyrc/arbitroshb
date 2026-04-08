from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ArbitroViewSet, PartidoViewSet,
    DisponibilidadViewSet, DesignacionViewSet,
    MiPerfilView, LiquidacionesExcelView,
    VapidPublicKeyView, PushSubscribeView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'arbitros', ArbitroViewSet)
router.register(r'partidos', PartidoViewSet)
router.register(r'disponibilidades', DisponibilidadViewSet)
router.register(r'designaciones', DesignacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('mi-perfil/', MiPerfilView.as_view(), name='mi-perfil'),
    path('liquidaciones/excel/', LiquidacionesExcelView.as_view(), name='liquidaciones-excel'),
    path('push/vapid-key/', VapidPublicKeyView.as_view(), name='vapid-public-key'),
    path('push/subscribe/', PushSubscribeView.as_view(), name='push-subscribe'),
]
