from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from .models import Rol, Usuario
from django.dispatch import receiver

User = get_user_model()

@receiver(post_migrate)
def setup_initial_data(sender, **kwargs):
    # 1. Crear Roles
    default_roles = [
        {'codigo': 'COR', 'nombre': 'Coordinacion'},
        {'codigo': 'EDIF', 'nombre': 'Administrador de Edificios'},
        {'codigo': 'INS', 'nombre': 'Instructor'},
        {'codigo': 'APR', 'nombre': 'Aprendiz'},
        {'codigo': 'ADM', 'nombre': 'Administrador'},  # Nuevo rol para el superusuario
    ]
    for rol in default_roles:
        Rol.objects.get_or_create(codigo=rol['codigo'], defaults={'nombre': rol['nombre']})

    # 2. Crear Grupos y asignar permisos
    roles_perms = {
        'Coordinacion': Permission.objects.all(),
        'Administrador de Edificios': ['add_novedad', 'change_novedad'],
        'Instructor': ['add_novedad'],
        'Aprendiz': [],
    }

    for name, perms in roles_perms.items():
        group, _ = Group.objects.get_or_create(name=name)
        group.permissions.clear()
        if perms == Permission.objects.all():
            group.permissions.set(perms)
        else:
            for codename in perms:
                try:
                    p = Permission.objects.get(codename=codename)
                    group.permissions.add(p)
                except Permission.DoesNotExist:
                    continue

    # 3. Crear superusuario si no existe
    if not User.objects.filter(username=settings.DEFAULT_ADMIN_USERNAME).exists():
        try:
            rol_admin = Rol.objects.get(codigo='ADM')
            admin = User.objects.create_superuser(
                username=settings.DEFAULT_ADMIN_USERNAME,
                email=settings.DEFAULT_ADMIN_EMAIL,
                password=settings.DEFAULT_ADMIN_PASSWORD,
                rol=rol_admin
            )
            coord_group = Group.objects.get(name='Coordinacion')
            admin.groups.add(coord_group)
        except Rol.DoesNotExist:
            print("Rol 'ADM' no existe. Verifica que esté definido correctamente.")