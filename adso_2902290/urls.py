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
from django.contrib import admin
from django.urls import path, include
from adso_2902290.views import *
from adso_app.views import login_view


urlpatterns = [
    #APi
    path('api_regional', include('adso_app.urls')),
    
    path('', login_view, name='login'),
    path('admin/', admin.site.urls),
    path('adso_app/', include('adso_app.urls')),
    path('base/', base, name='base'),
    path('rol/insertar/', insertar_rol, name='insertar_rol'),
    path('rol/listar/', listar_rol,name='listar_rol'),
    path('rol/actualizar/<int:id>/',actualizar_rol,name='actualizar_rol'),
    path('rol/eliminar/<int:id>/',eliminar_rol,name='eliminar_rol'),
    path('usuario/insertar/', insertar_usuario, name='insertar_usuario'),
    path('usuario/listar/', listar_usuario,name='listar_usuario'),
    path('usuario/actualizar/<int:id>/',actualizar_usuario,name='actualizar_usuario'),
    path('usuario/eliminar/<int:id>/',eliminar_usuario,name='eliminar_usuario'),

# regional
    path('regional/insertar/', insertar_regional, name='insertar_regional'),
    path('regional/listar/', listar_regional,name='listar_regional'),
    path('regional/actualizar/<int:id>/',actualizar_regional,name='actualizar_regional'),
    path('regional/eliminar/<int:id>/',eliminar_regional,name='eliminar_regional'),


# centro de formacion
    path('centro_formacion/insertar/', insertar_centro_formacion, name='insertar_centro_formacion'),
    path('centro_formacion/listar', listar_centro_formacion,name='listar_centro_formacion'),
    path('centro_formacion/actualizar/<int:id>/',actualizar_centro_formacion,name='actualizar_centro_formacion'),
    path('centro_formacion/eliminar/<int:id>/',eliminar_centro_formacion,name='eliminar_centro_formacion'),





    path('sede/insertar/', insertar_sede, name='insertar_sede'),
    path('sede/listar', listar_sede,name='listar_sede'),
    path('sede/actualizar/<int:id>/',actualizar_sede,name='actualizar_sede'),
    path('sede/eliminar/<int:id>/',eliminar_sede,name='eliminar_sede'),





    path('tipo_ambiente/insertar/', insertar_tipo_ambiente, name='insertar_tipo_ambiente'),
    path('tipo_ambiente/listar', listar_tipo_ambiente,name='listar_tipo_ambiente'),
    path('tipo_ambiente/actualizar/<int:id>/',actualizar_tipo_ambiente,name='actualizar_tipo_ambiente'),
    path('tipo_ambiente/eliminar/<int:id>/',eliminar_tipo_ambiente,name='eliminar_tipo_ambiente'),




    path('ambiente/insertar/', insertar_ambiente, name='insertar_ambiente'),
    path('ambiente/listar', listar_ambiente,name='listar_ambiente'),
    path('ambiente/actualizar/<int:id>/',actualizar_ambiente,name='actualizar_ambiente'),
    path('ambiente/eliminar/<int:id>/',eliminar_ambiente,name='eliminar_ambiente'),




    path('tipo_mobiliario/insertar/', insertar_tipo_mobiliario, name='insertar_tipo_mobiliario'),
    path('tipo_mobiliario/listar', listar_tipo_mobiliario,name='listar_tipo_mobiliario'),
    path('tipo_mobiliario/actualizar/<int:id>/',actualizar_tipo_mobiliario,name='actualizar_tipo_mobiliario'),
    path('tipo_mobiliario/eliminar/<int:id>/',eliminar_tipo_mobiliario,name='eliminar_tipo_mobiliario'),





    path('mobiliario/insertar/', insertar_mobiliario, name='insertar_mobiliario'),
    path('mobiliario/listar', listar_mobiliario,name='listar_mobiliario'),
    path('mobiliario/actualizar/<int:id>/',actualizar_mobiliario,name='actualizar_mobiliario'),
    path('mobiliario/eliminar/<int:id>/',eliminar_mobiliario,name='eliminar_mobiliario'),

    

]
