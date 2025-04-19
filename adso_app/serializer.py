from rest_framework import serializers
from .models import *

class RegionalSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Regional
        fields='__all__'

class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sede
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Usuario
        fields='__all__'

class CentroSerializer(serializers.ModelSerializer):
    class Meta:
        model=CentroFormacion
        fields='__all__'

class TipoAmbientesSerializer(serializers.ModelSerializer):
    class Meta:
        model=TipoAmbiente
        fields='__all__'

class AmbienteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ambiente
        fields='__all__'

class TipoMobiliarioSerializer(serializers.ModelSerializer):
    class Meta:
        model=TipoMobiliario
        fields='__all__'

class MobiliarioSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mobiliario
        fields='__all__'