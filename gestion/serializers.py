from rest_framework import serializers
from .models import CustomUser, Arbitro, Partido, Disponibilidad, Designacion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class ArbitroSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = Arbitro
        fields = ['id', 'user', 'user_id', 'phone', 'category']

class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = '__all__'

class DisponibilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilidad
        fields = '__all__'

class DesignacionSerializer(serializers.ModelSerializer):
    partido_detail = PartidoSerializer(source='partido', read_only=True)
    arbitro_detail = ArbitroSerializer(source='arbitro', read_only=True)

    class Meta:
        model = Designacion
        fields = ['id', 'partido', 'arbitro', 'status', 'created_at', 'partido_detail', 'arbitro_detail']
