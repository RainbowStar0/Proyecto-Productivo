from django import forms
from .models import Usuario, Ficha, Programa, Mobiliario, Novedad
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
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class NovedadForm(forms.ModelForm):
    class Meta:
        model = Novedad
        fields = ['tipo', 'aprendiz', 'sede', 'ambiente', 'descripcion']
        

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

