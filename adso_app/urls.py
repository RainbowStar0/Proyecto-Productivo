"""
URL configuration for adso_2902290 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework import routers
from adso_app.views import RegionalViewSet
from .views import (
    login_view, register_view, CustomLogoutView,
    insertar_novedad, listar_novedades, actualizar_novedad
)


router=routers.DefaultRouter()
router.register(r'regionalesrest', RegionalViewSet)

urlpatterns = [
    path('/regionales/', include(router.urls)),
    
    path('register/', register_view, name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # <- ESTA ES LA IMPORTANTE  
    path('novedades/insertar/', insertar_novedad, name='insertar_novedad'),
    path('novedades/', listar_novedades, name='listar_novedades'),
    path('novedades/<int:pk>/editar/', actualizar_novedad, name='actualizar_novedad'),
]