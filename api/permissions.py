from rest_framework.permissions import BasePermission
from .models import Jardinero, Cliente


class IsJardinero(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'perfil_jardinero')


class IsClienteOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.cliente == request.user.perfil_cliente
