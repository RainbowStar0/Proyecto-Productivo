from django.contrib import admin
from .models import (
    Usuario, Rol,
    Regional, CentroFormacion, Sede,
    TipoAmbiente, Ambiente,
    TipoMobiliario, Mobiliario,
    Programa, Ficha
)

admin.site.register(Usuario)
admin.site.register(Rol)
admin.site.register(Regional)
admin.site.register(CentroFormacion)
admin.site.register(Sede)
admin.site.register(TipoAmbiente)
admin.site.register(Ambiente)
admin.site.register(TipoMobiliario)
admin.site.register(Mobiliario)
admin.site.register(Programa)
admin.site.register(Ficha)
