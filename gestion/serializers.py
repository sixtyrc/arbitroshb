from rest_framework import serializers
from .models import CustomUser, Arbitro, Partido, Disponibilidad, Designacion, Categoria, CategoriaGrupo, Arancel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ArbitroSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Arbitro
        fields = ['id', 'user', 'phone', 'categoria_max']

class PartidoSerializer(serializers.ModelSerializer):
    categoria_detail = CategoriaSerializer(source='categoria', read_only=True)
    class Meta:
        model = Partido
        fields = ['id', 'title', 'categoria', 'categoria_detail', 'date_time', 'location']

class DisponibilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilidad
        fields = '__all__'

class DesignacionSerializer(serializers.ModelSerializer):
    partido_detail = PartidoSerializer(source='partido', read_only=True)
    arbitro_detail = ArbitroSerializer(source='arbitro', read_only=True)
    monto_honorario = serializers.ReadOnlyField() # Propiedad calculada en el modelo

    class Meta:
        model = Designacion
        fields = [
            'id', 'partido', 'arbitro', 'status', 'rol_asignado', 
            'monto_honorario', 'created_at', 'partido_detail', 'arbitro_detail'
        ]
