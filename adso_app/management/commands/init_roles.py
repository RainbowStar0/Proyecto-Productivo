# adso_app/management/commands/init_roles.py

from django.core.management.base import BaseCommand
from adso_app.models import Rol

class Command(BaseCommand):
    help = 'Inicializa los roles principales del sistema'

    def handle(self, *args, **kwargs):
        roles = [
            {'codigo': 'aprendiz', 'nombre': 'Aprendiz', 'descripcion': 'Rol por defecto. Solo lectura de novedades propias.'},
            {'codigo': 'instructor', 'nombre': 'Instructor', 'descripcion': 'Puede registrar y ver novedades de sus fichas.'},
            {'codigo': 'coordinador', 'nombre': 'Coordinador', 'descripcion': 'Control total del sistema.'},
            {'codigo': 'admin_edificios', 'nombre': 'Administrador de Edificios', 'descripcion': 'Agrega información a novedades de ambiente.'}
        ]

        for r in roles:
            try:
                obj, created = Rol.objects.get_or_create(codigo=r['codigo'], defaults={
                    'nombre': r['nombre'],
                    'descripcion': r['descripcion']
                })
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Rol '{r['nombre']}' creado."))
                else:
                    self.stdout.write(self.style.WARNING(f"Rol '{r['nombre']}' ya existe."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error al crear rol '{r['nombre']}': {str(e)}"))
