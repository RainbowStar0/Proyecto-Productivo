from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models.signals import pre_save
import os


# ========================
# ROLES Y USUARIOS
# ========================

class Rol(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nombre

class Regional(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nombre

class CentroFormacion(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=255, null=False)
    telefono = models.CharField(max_length=255, null=False)
    regional = models.ForeignKey(Regional, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class Sede(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=255, null=False)
    centro_de_formacion = models.ForeignKey(CentroFormacion, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombre

class Usuario(AbstractUser):
    class TipoDoc(models.TextChoices):
        TI = 'TI', 'Tarjeta de identidad'
        CC = 'CC', 'Cédula de ciudadanía'
        CE = 'CE', 'Cédula de extranjería'
        PPT = 'PPT', 'Permiso de protección especial'

    tipo_doc = models.CharField(max_length=3, choices=TipoDoc.choices, default=TipoDoc.CC)
    numero_documento = models.CharField(max_length=12)
    telefono = models.CharField(max_length=30, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    regional = models.ForeignKey(Regional, null=True, blank=True, on_delete=models.SET_NULL)
    sede = models.ForeignKey(Sede, null=True, blank=True, on_delete=models.SET_NULL)
    centro_form = models.ForeignKey(CentroFormacion, null=True, blank=True, on_delete=models.SET_NULL)
    programa = models.ForeignKey('Programa', null=True, blank=True, on_delete=models.SET_NULL)
    ficha = models.ForeignKey('Ficha', null=True, blank=True, on_delete=models.SET_NULL)


# ========================
# NOVEDADES
# ========================

class Ambiente(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'AC', 'Activo'
        INACTIVO = 'IN', 'Inactivo'

    codigo = models.CharField(max_length=100, null=False, unique=True)
    estado = models.CharField(
        max_length=2,
        choices=Estado.choices,
        default=Estado.ACTIVO
    )
    ubicacion = models.CharField(max_length=255, null=False)
    tipo_ambiente = models.ForeignKey('TipoAmbiente', on_delete=models.PROTECT)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.codigo} - {self.sede.nombre}"


class Novedad(models.Model):
    TIPO = [
        ('ACAD', 'Académica'),
        ('DISC', 'Disciplinaria'),
        ('AMBI', 'Ambiente'),
    ]
    tipo = models.CharField(max_length=4, choices=TIPO)
    aprendiz = models.ForeignKey(Usuario, related_name='novedades', on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT)
    ambiente = models.ForeignKey(Ambiente, null=True, blank=True, on_delete=models.SET_NULL)
    descripcion = models.TextField()
    creado_por = models.ForeignKey(Usuario, related_name='creadas', on_delete=models.SET_NULL, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='evidencias/')

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.aprendiz.username}"

@receiver(post_delete, sender=Novedad)
def eliminar_archivo_disco(sender, instance, **kwargs):
        if instance.archivo and os.path.isfile(instance.archivo.path):
            os.remove(instance.archivo.path)

@receiver(pre_save, sender=Novedad)
def eliminar_archivo_anterior_al_actualizar(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_file = Novedad.objects.get(pk=instance.pk).archivo
    except Novedad.DoesNotExist:
        return

    new_file = instance.archivo
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

# ========================
# AMBIENTES Y MOBILIARIO
# ========================

class TipoAmbiente(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nombre

class TipoMobiliario(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    descripcion = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.descripcion

class Mobiliario(models.Model):
    placa = models.CharField(max_length=100, null=False, unique=True)
    modelo = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=500, null=False)
    atributos = models.CharField(max_length=300, null=False)
    observaciones = models.CharField(max_length=500, null=False)
    fecha_adquisicion = models.DateField(null=False)
    valor_ingreso = models.DecimalField(max_digits=65, decimal_places=2, null=False)
    ambiente = models.ForeignKey(Ambiente, on_delete=models.PROTECT)
    tipo = models.ForeignKey(TipoMobiliario, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.placa} - {self.modelo}"

# ========================
# PROGRAMAS Y FICHAS
# ========================
class Ficha(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    jornada = models.CharField(max_length=10, choices=[('diurno', 'Diurno'), ('nocturno', 'Nocturno')])

    def __str__(self):
        return self.codigo

class Programa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} - {self.ficha.codigo}"