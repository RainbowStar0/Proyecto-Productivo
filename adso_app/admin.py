from django.contrib import admin
from .models import Usuario, Rol, Novedad
from django.contrib.auth.admin import UserAdmin

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre')

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Datos Adicionales', {
            'fields': (
                'tipo_doc', 'numero_documento', 'telefono', 'rol',
                'regional', 'sede', 'centro_form', 'programa', 'ficha'
            )
        }),
    )
    list_display = ('username', 'email', 'rol', 'sede')

@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'aprendiz', 'sede', 'creado_por', 'creado_en')
    list_filter = ('tipo', 'sede')