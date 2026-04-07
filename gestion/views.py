from rest_framework import viewsets, permissions
from .models import CustomUser, Arbitro, Partido, Disponibilidad, Designacion
from .serializers import UserSerializer, ArbitroSerializer, PartidoSerializer, DisponibilidadSerializer, DesignacionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ArbitroViewSet(viewsets.ModelViewSet):
    queryset = Arbitro.objects.all()
    serializer_class = ArbitroSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class PartidoViewSet(viewsets.ModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

class DisponibilidadViewSet(viewsets.ModelViewSet):
    queryset = Disponibilidad.objects.all()
    serializer_class = DisponibilidadSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Disponibilidad.objects.all()
        return Disponibilidad.objects.filter(arbitro__user=user)

class DesignacionViewSet(viewsets.ModelViewSet):
    queryset = Designacion.objects.all()
    serializer_class = DesignacionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Designacion.objects.all()
        return Designacion.objects.filter(arbitro__user=user)
