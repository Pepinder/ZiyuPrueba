from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Jardinero, Cliente, SolicitudVisita


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ClienteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'user', 'telefono']


class JardineroSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Jardinero
        fields = ['id', 'user', 'especialidad']


class SolicitudVisitaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    jardinero_asignado = JardineroSerializer(read_only=True)

    estado = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = SolicitudVisita
        fields = [
            'id', 'cliente', 'jardinero_asignado', 'direccion', 'tipo_servicio',
            'disponibilidad_horaria', 'metros_cuadrados', 'latitud', 'longitud',
            'estado', 'fecha_creacion', 'fecha_visita_confirmada'
        ]
        read_only_fields = ['id', 'cliente', 'jardinero_asignado',
                            'estado', 'fecha_creacion', 'fecha_visita_confirmada']


class AsignarJardineroSerializer(serializers.ModelSerializer):
    jardinero_id = serializers.IntegerField()

    def validate_jardinero_id(self, value):
        try:
            jardinero = Jardinero.objects.get(id=value)
        except Jardinero.DoesNotExist:
            raise serializers.ValidationError(
                "El jardinero con el ID proporcionado no existe.")
        return value

# class AsignarJardineroSerializer(serializers.Serializer):
#     jardinero_id = serializers.IntegerField()

#     def validate_jardinero_id(self, value):
#         if not Jardinero.objects.filter(id=value).exists():
#             raise serializers.ValidationError("El perfil de Jardinero especificado no existe.")
#         return value

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    rol = serializers.ChoiceField(choices=[('cliente', 'Cliente'), ('jardinero', 'Jardinero')], write_only=True)
    
    # Campos opcionales para los perfiles
    telefono = serializers.CharField(required=False, write_only=True)
    especialidad = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'rol', 'telefono', 'especialidad')

    def create(self, validated_data):
        # Extraemos los datos del perfil y el rol
        rol = validated_data.pop('rol')
        telefono = validated_data.pop('telefono', None)
        especialidad = validated_data.pop('especialidad', None)
        
        # Creamos el usuario
        user = User.objects.create_user(**validated_data)
        
        # Creamos el perfil asociado según el rol
        if rol == 'cliente':
            Cliente.objects.create(user=user, telefono=telefono or '')
        elif rol == 'jardinero':
            Jardinero.objects.create(user=user, especialidad=especialidad or '')
            
        return user