from adso_app.models import Regional
from adso_app.serializer import RegionalSerializer
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .forms import LoginForm, RegistrationForm, NovedadForm
from .models import Novedad
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import Rol




class RegionalViewSet(viewsets.ModelViewSet):
    queryset=Regional.objects.all()
    serializer_class=RegionalSerializer
    



# Helpers
def in_group(user, groups):
    return user.is_authenticated and user.groups.filter(name__in=groups).exists()

# Login & Logout Views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('listar_novedades')
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, 'Has iniciado sesión correctamente.')
        return redirect('listar_novedades')
    if request.method == 'POST':
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('listar_novedades')

    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        # asigna el Rol 'Aprendiz'
        rol_aprendiz = Rol.objects.get(codigo='APR')
        user.rol = rol_aprendiz
        user.save()
        # agrégalo al grupo de permisos
        grupo = Group.objects.get(name='Aprendiz')
        user.groups.add(grupo)

        messages.success(request, '¡Cuenta creada! Ahora inicia sesión.')
        return redirect('login')
    elif request.method == 'POST':
        messages.error(request, 'Hubo un error creando la cuenta. Revisa los datos.')

    return render(request, 'register.html', {'form': form})

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Sesión cerrada correctamente.')
        return super().dispatch(request, *args, **kwargs)

# Novedades Views
@login_required
@user_passes_test(lambda u: in_group(u, ['Instructor', 'Edificios', 'Coordinacion']))
def insertar_novedad(request):
    form = NovedadForm(request.POST or None)
    if form.is_valid():
        nov = form.save(commit=False)
        nov.creado_por = request.user
        if in_group(request.user, ['Edificios']):
            nov.sede = request.user.sede
        nov.save()
        return redirect('listar_novedades')
    return render(request, 'novedades/insertar.html', {'form': form})

@login_required
def listar_novedades(request):
    # Aprendiz ve solo sus propias novedades
    if in_group(request.user, ['Aprendiz']):
        novedades = Novedad.objects.filter(aprendiz=request.user)
    else:
        novedades = Novedad.objects.all()
    return render(request, 'novedades/listar.html', {'novedades': novedades})

@login_required
@user_passes_test(lambda u: in_group(u, ['Coordinacion']))
def actualizar_novedad(request, pk):
    nov = get_object_or_404(Novedad, pk=pk)
    form = NovedadForm(request.POST or None, instance=nov)
    if form.is_valid():
        form.save()
        return redirect('listar_novedades')
    return render(request, 'novedades/actualizar.html', {'form': form})