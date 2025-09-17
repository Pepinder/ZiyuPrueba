from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SolicitudVisitaViewSet, UserRegisterView

router = DefaultRouter()
router.register(r'solicitudes', SolicitudVisitaViewSet, basename='solicitud')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='user-register'),
]
