# api/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import SolicitudVisita, Cliente, Jardinero
from .serializers import SolicitudVisitaSerializer, AsignarJardineroSerializer
from .permissions import IsJardinero, IsClienteOwner
from django.db import models
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer
from django.contrib.auth.models import User


class SolicitudVisitaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar las solicitudes de visita.
    - Clientes: Crean y ven sus solicitudes.
    - Jardineros: Ven solicitudes disponibles ('solicitada') y se asignan a ellas.
    - Admin (Empresa): Ven todo y pueden asignar jardineros manualmente.
    """
    queryset = SolicitudVisita.objects.all().select_related(
        'cliente__user', 'jardinero_asignado__user').order_by('-fecha_creacion')
    serializer_class = SolicitudVisitaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return super().get_queryset()

        elif hasattr(user, 'perfil_jardinero'):
            return SolicitudVisita.objects.filter(
                models.Q(estado=SolicitudVisita.ESTADO_SOLICITADA) |
                models.Q(jardinero_asignado=user.perfil_jardinero)
            )

        elif hasattr(user, 'perfil_cliente'):
            return SolicitudVisita.objects.filter(cliente=user.perfil_cliente)

        return SolicitudVisita.objects.none()

    def perform_create(self, serializer):
        # Asignar automáticamente el cliente al crear la solicitud
        serializer.save(cliente=self.request.user.perfil_cliente)

    @action(detail=True, methods=['post'], url_path='aceptar-servicio', permission_classes=[IsJardinero])
    def aceptar_servicio(self, request, pk=None):

        # Acción para que un jardinero se asigne a sí mismo a una solicitud disponible.

        solicitud = self.get_object()

        if solicitud.estado != SolicitudVisita.ESTADO_SOLICITADA:
            return Response({'error': 'Esta solicitud ya no está disponible.'}, status=status.HTTP_400_BAD_REQUEST)

        jardinero_actual = request.user.perfil_jardinero
        solicitud.jardinero_asignado = jardinero_actual
        solicitud.estado = SolicitudVisita.ESTADO_ASIGNADA
        solicitud.save()

        serializer = self.get_serializer(solicitud)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='confirmar-visita', permission_classes=[IsClienteOwner])
    def confirmar_visita(self, request, pk=None):
        solicitud = self.get_object()

        if solicitud.estado != SolicitudVisita.ESTADO_ASIGNADA:
            return Response({'error': 'La solicitud no puede ser confirmada en su estado actual.'}, status=status.HTTP_400_BAD_REQUEST)

        solicitud.estado = SolicitudVisita.ESTADO_CONFIRMADA
        solicitud.save()
        return Response({'status': 'Visita confirmada por el cliente'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='asignar-jardinero-admin', permission_classes=[IsAdminUser])
    def asignar_jardinero_admin(self, request, pk=None):

        solicitud = self.get_object()
        serializer = AsignarJardineroSerializer(data=request.data)

        if serializer.is_valid():
            jardinero = Jardinero.objects.get(
                id=serializer.validated_data['jardinero_id'])
            solicitud.jardinero_asignado = jardinero
            solicitud.estado = SolicitudVisita.ESTADO_ASIGNADA
            solicitud.save()
            return Response({'status': 'Jardinero asignado por el administrador'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(generics.CreateAPIView):
    """
    Endpoint para el registro de nuevos usuarios (Clientes o Jardineros).
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]  # Cualquiera puede registrarse
