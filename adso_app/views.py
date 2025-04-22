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
        return redirect('base')
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, 'Has iniciado sesión correctamente.')
        return redirect('base')
    if request.method == 'POST':
        messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('base')

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

from django.shortcuts import render, redirect, get_object_or_404
from .models import Ficha, Programa
from .forms import FichaForm, ProgramaForm

# === FICHA ===
def insertar_ficha(request):
    form = FichaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_fichas')
    return render(request, 'ficha/insertar.html', {'form': form})

def actualizar_ficha(request, pk):
    ficha = get_object_or_404(Ficha, pk=pk)
    form = FichaForm(request.POST or None, instance=ficha)
    if form.is_valid():
        form.save()
        return redirect('listar_fichas')
    return render(request, 'ficha/actualizar.html', {'form': form})

def listar_fichas(request):
    fichas = Ficha.objects.all()
    return render(request, 'ficha/listar.html', {'fichas': fichas})

# === PROGRAMA ===
def insertar_programa(request):
    form = ProgramaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_programas')
    return render(request, 'programa_formacion/insertar.html', {'form': form})

def actualizar_programa(request, pk):
    programa = get_object_or_404(Programa, pk=pk)
    form = ProgramaForm(request.POST or None, instance=programa)
    if form.is_valid():
        form.save()
        return redirect('listar_programas')
    return render(request, 'programa_formacion/actualizar.html', {'form': form})

def listar_programas(request):
    programas = Programa.objects.all()
    return render(request, 'programa_formacion/listar.html', {'programas': programas})
