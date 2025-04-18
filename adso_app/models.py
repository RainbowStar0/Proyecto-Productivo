from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Rol(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=255, null=False, default='instructor')

class Usuario(AbstractUser):
    TIPO_DOC = [
        ('TI','Targeta de identidad'),
        ('CC','Cedula de ciudadania'),
        ('CE','Cedula de extranjeria'),
        ('PPT','Permiso de proteccion especial')
    ]
    tipo_doc = models.CharField(max_length=3, choices=TIPO_DOC, default='CC')
    numero_documento = models.CharField(max_length=12, null=False)
    telefono = models.CharField(max_length=30, blank=True, null=False)
    rol = models.ForeignKey(Rol,on_delete=models.PROTECT)

class Regional(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)

class Centro_formacion(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=255, null=False)
    telefono = models.CharField(max_length=255, null=False)
    regional = models.ForeignKey(Regional,on_delete=models.PROTECT)

class Sede(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=255, null=False)
    centro_de_formacion = models.ForeignKey(Centro_formacion,on_delete=models.PROTECT)

class Tipo_ambiente(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    nombre = models.CharField(max_length=100, null=False)

class Ambiente(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    estado = models.CharField(max_length=100, null=False)
    ubicacion = models.CharField(max_length=255, null=False)
    tipo_ambiente = models.ForeignKey(Tipo_ambiente,on_delete=models.PROTECT)
    sede = models.ForeignKey(Sede,on_delete=models.PROTECT)


class Tipo_mobiliario(models.Model):
    codigo = models.CharField(max_length=100, null=False, unique=True)
    descripcion = models.CharField(max_length=100, null=False)

class Mobiliario(models.Model):
    placa = models.CharField(max_length=100, null=False, unique=True)
    modelo = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=500, null=False)
    atributos = models.CharField(max_length=300, null=False)
    observaciones = models.CharField(max_length=500, null=False)
    fecha_adquisicion = models.DateField(null=False)
    valor_ingreso = models.DecimalField(max_digits=65,decimal_places=2, null=False)
    ambiente = models.ForeignKey(Ambiente,on_delete=models.PROTECT)
    tipo = models.ForeignKey(Tipo_mobiliario,on_delete=models.PROTECT)

