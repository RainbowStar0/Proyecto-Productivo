from rest_framework import serializers
from .models import Regional

class RegionalSerializer(serializers.ModelSerializer):
    class Meta: 
        model=Regional
        fields='__all__'