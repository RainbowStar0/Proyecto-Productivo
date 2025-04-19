from django.db import models
from django.contrib.auth.models import AbstractUser


# ========================
# ROLES Y USUARIOS
# ========================

class Rol(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=255, null=False, default='instructor')

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    TIPO_DOC = [
        ('TI', 'Tarjeta de identidad'),
        ('CC', 'Cédula de ciudadanía'),
        ('CE', 'Cédula de extranjería'),
        ('PPT', 'Permiso de protección temporal'),
    ]
    tipo_doc = models.CharField(max_length=3, choices=TIPO_DOC, default='CC')
    numero_documento = models.CharField(max_length=12, null=False)
    telefono = models.CharField(max_length=30, blank=True, null=False, default='N/A')
    
    # Cambiar para asignar un valor por defecto
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, default=None)

    ficha = models.ForeignKey('Ficha', on_delete=models.SET_NULL, null=True, blank=True)
    fichas_instructor = models.ManyToManyField('Ficha', related_name='instructores', blank=True)
    sede = models.ForeignKey('Sede', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"

# ========================
# ESTRUCTURA INSTITUCIONAL
# ========================

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


# ========================
# AMBIENTES Y MOBILIARIO
# ========================

class TipoAmbiente(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nombre


class Ambiente(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    estado = models.CharField(max_length=100, null=False)
    ubicacion = models.CharField(max_length=255, null=False)
    tipo_ambiente = models.ForeignKey(TipoAmbiente, on_delete=models.PROTECT)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.codigo} - {self.sede.nombre}"


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

class Programa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Ficha(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
    jornada = models.CharField(max_length=10, choices=[('diurno', 'Diurno'), ('nocturno', 'Nocturno')])

    def __str__(self):
        return f"{self.codigo} - {self.programa.nombre}"
