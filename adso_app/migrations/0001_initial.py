# Generated by Django 5.1.7 on 2025-04-19 00:13

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Regional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100, unique=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(default='instructor', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TipoAmbiente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100, unique=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoMobiliario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CentroFormacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=255)),
                ('regional', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adso_app.regional')),
            ],
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('centro_de_formacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adso_app.centroformacion')),
            ],
        ),
        migrations.CreateModel(
            name='Ficha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50, unique=True)),
                ('jornada', models.CharField(choices=[('diurno', 'Diurno'), ('nocturno', 'Nocturno')], max_length=10)),
                ('programa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adso_app.programa')),
                ('sede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adso_app.sede')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('tipo_doc', models.CharField(choices=[('TI', 'Tarjeta de identidad'), ('CC', 'Cédula de ciudadanía'), ('CE', 'Cédula de extranjería'), ('PPT', 'Permiso de protección temporal')], default='CC', max_length=3)),
                ('numero_documento', models.CharField(max_length=12, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=30, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('ficha', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adso_app.ficha')),
                ('fichas_instructor', models.ManyToManyField(blank=True, related_name='instructores', to='adso_app.ficha')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adso_app.rol')),
                ('sede', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adso_app.sede')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ambiente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=100, unique=True)),
                ('estado', models.CharField(max_length=100)),
                ('ubicacion', models.CharField(max_length=255)),
                ('sede', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adso_app.sede')),
                ('tipo_ambiente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adso_app.tipoambiente')),
            ],
        ),
        migrations.CreateModel(
            name='Mobiliario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=100, unique=True)),
                ('modelo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=500)),
                ('atributos', models.CharField(max_length=300)),
                ('observaciones', models.CharField(max_length=500)),
                ('fecha_adquisicion', models.DateField()),
                ('valor_ingreso', models.DecimalField(decimal_places=2, max_digits=65)),
                ('ambiente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adso_app.ambiente')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='adso_app.tipomobiliario')),
            ],
        ),
    ]
