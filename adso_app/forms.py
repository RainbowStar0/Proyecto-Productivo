from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        # Quitamos 'rol' del listado de campos
        fields = [
            'tipo_doc',
            'numero_documento',
            'first_name',
            'last_name',
            'username',
            'telefono',
            'email',
            'password',
        ]


class UsuarioRegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        exclude = ['rol', 'ficha', 'fichas_instructor', 'sede', 'last_login', 'date_joined', 'is_staff', 'is_superuser', 'user_permissions', 'groups']




class LoginForm(AuthenticationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
    }

class NovedadForm(forms.ModelForm):
    class Meta:
        model = Novedad
        fields = ['tipo', 'aprendiz', 'sede', 'ambiente', 'descripcion']
        widgets = { # se añadio
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'ambiente': forms.Select(attrs={'class': 'form-control'}),
            'aprendiz': forms.Select(attrs={'class': 'form-control'})
            }
        

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']
        widgets = { # se añadio
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        }

class NovedadForm(forms.ModelForm):
    class Meta:
        model = Novedad
        fields = ['tipo', 'aprendiz', 'sede', 'ambiente', 'descripcion', 'archivo']
        widgets = { # se añadio
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'ambiente': forms.Select(attrs={'class': 'form-control'}),
            'aprendiz': forms.Select(attrs={'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }