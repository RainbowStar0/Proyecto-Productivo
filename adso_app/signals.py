from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Usuario, Rol

@receiver(post_save, sender=Usuario)
def asignar_rol_aprendiz(sender, instance, created, **kwargs):
    if created and not instance.rol:
        try:
            # Intentamos obtener el rol 'Aprendiz'
            aprendiz = Rol.objects.get(nombre__iexact='Aprendiz')
            instance.rol = aprendiz
            instance.save()
        except Rol.DoesNotExist:
            # Si no existe el rol 'Aprendiz', se lanza un mensaje en consola
            print("El rol 'Aprendiz' no existe. Debe crearse primero.")
