from django.contrib import admin
from .models import Jardinero, Cliente, SolicitudVisita

# Register your models here.
admin.site.register(Jardinero)
admin.site.register(Cliente)
admin.site.register(SolicitudVisita)
