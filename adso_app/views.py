from adso_app.models import Regional
from adso_app.serializer import RegionalSerializer
from rest_framework import viewsets

class RegionalViewSet(viewsets.ModelViewSet):
    queryset=Regional.objects.all()
    serializer_class=RegionalSerializer