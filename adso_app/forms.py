from django import forms
from .models import Usuario, Ficha, Programa, Mobiliario
from django import forms
from .models import Usuario, Ficha, Programa, Mobiliario

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

