from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from .models import Rol

User = get_user_model()

def create_roles():
    default_roles = [
        {'codigo': 'COR',    'nombre': 'Coordinacion'},
        {'codigo': 'EDIF',   'nombre': 'Administrador de Edificios'},
        {'codigo': 'INS',    'nombre': 'Instructor'},
        {'codigo': 'APR',    'nombre': 'Aprendiz'},
    ]
    for r in default_roles:
        Rol.objects.get_or_create(codigo=r['codigo'], defaults={'nombre': r['nombre']})

def create_default_admin():
    if not User.objects.filter(username=settings.DEFAULT_ADMIN_USERNAME).exists():
        rol_coordinacion = Rol.objects.get(codigo='COR')
        admin = User.objects.create_superuser(
            username=settings.DEFAULT_ADMIN_USERNAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=settings.DEFAULT_ADMIN_PASSWORD,
            rol=rol_coordinacion
        )
        grp = Group.objects.get(name='Coordinacion')
        admin.groups.add(grp)

def create_groups_and_admin(sender, **kwargs):
    # 1) Crear roles en la tabla Rol
    create_roles()

    # 2) Crear/ajustar Groups y permisos
    roles_perms = {
        'Coordinacion': Permission.objects.all(),
        'Edificios':    ['add_novedad', 'change_novedad'],
        'Instructor':   ['add_novedad'],
        'Aprendiz':     [],
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
                    pass

    # 3) Crear el superusuario con rol ya asignado
    create_default_admin()

class AdsoAppConfig(AppConfig):
    name = 'adso_app'

    def ready(self):
        post_migrate.connect(create_groups_and_admin, sender=self)


User = get_user_model()

def create_default_admin():
    if not User.objects.filter(username=settings.DEFAULT_ADMIN_USERNAME).exists():
        admin = User.objects.create_superuser(
            username=settings.DEFAULT_ADMIN_USERNAME,
            email=settings.DEFAULT_ADMIN_EMAIL,
            password=settings.DEFAULT_ADMIN_PASSWORD
        )
        coord_group = Group.objects.get(name='Coordinacion')
        admin.groups.add(coord_group)

class AdsoAppConfig(AppConfig):
    name = 'adso_app'

    def ready(self):
        post_migrate.connect(create_groups_and_admin, sender=self)


def create_groups_and_admin(sender, **kwargs):
    roles = {
        'Coordinacion': Permission.objects.all(),
        'Edificios': ['add_novedad'],
        'Instructor': ['add_novedad'],
        'Aprendiz': [],
    }
    for name, perms in roles.items():
        group, _ = Group.objects.get_or_create(name=name)
        group.permissions.clear()
        if perms == Permission.objects.all():
            group.permissions.set(Permission.objects.all())
        else:
            for codename in perms:
                try:
                    p = Permission.objects.get(codename=codename)
                    group.permissions.add(p)
                except Permission.DoesNotExist:
                    pass

    create_default_admin()
    
User = get_user_model()

