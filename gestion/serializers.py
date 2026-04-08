from rest_framework import serializers
from .models import CustomUser, Arbitro, Partido, Disponibilidad, Designacion, Categoria, CategoriaGrupo, Arancel

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ArbitroSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Arbitro
        fields = ['id', 'user', 'phone', 'cbu_alias', 'categoria_max']

class ArbitroProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer que el árbitro usa para actualizar su propio perfil."""
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Arbitro
        fields = ['first_name', 'last_name', 'email', 'phone', 'cbu_alias']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

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
