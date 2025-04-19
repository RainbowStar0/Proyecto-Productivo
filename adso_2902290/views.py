from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from adso_app.models import *
from django.contrib.auth import login, logout, authenticate


def base(request):
    return render(request, 'base.html')


def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('base')
            else:
                return render(request, 'usuario/login.html', {'mensaje_error': 'Credenciales incorrectas'})
    return render(request, 'usuario/login.html')


def logout_usuario(request):
    logout(request)
    return redirect('base')


# ROL

def insertar_rol(request):
    if request.method == 'POST':
        if request.POST.get('nombre') and request.POST.get('descripcion') and request.POST.get('codigo'):
            Rol.objects.create(
                codigo=request.POST['codigo'],
                nombre=request.POST['nombre'],
                descripcion=request.POST['descripcion']
            )
            return redirect('listar_rol')
    return render(request, 'rol/insertar.html')


def listar_rol(request):
    roles = Rol.objects.all()
    total = roles.count()
    return render(request, 'rol/listar.html', {'rol': roles, 'total_roles': total})


def actualizar_rol(request, id):
    rol = get_object_or_404(Rol, id=id)
    if request.method == 'POST':
        if all(request.POST.get(field) for field in ['codigo', 'nombre', 'descripcion']):
            rol.codigo = request.POST['codigo']
            rol.nombre = request.POST['nombre']
            rol.descripcion = request.POST['descripcion']
            rol.save()
            return redirect('listar_rol')
    return render(request, 'rol/actualizar.html', {'rol': rol})


def eliminar_rol(request, id):
    rol = get_object_or_404(Rol, id=id)
    rol.delete()
    return redirect('listar_rol')


# USUARIO

def insertar_usuario(request):
    if request.method == 'POST':
        campos = ['tipo_doc', 'numero_documento', 'first_name', 'last_name', 'username', 'email', 'password', 'telefono', 'rol_id']
        if all(request.POST.get(campo) for campo in campos):
            usuario = Usuario.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                tipo_doc=request.POST['tipo_doc'],
                numero_documento=request.POST['numero_documento'],
                telefono=request.POST['telefono'],
                rol_id=request.POST['rol_id']
            )
            return redirect('listar_usuario')
    roles = Rol.objects.all()
    return render(request, 'usuario/insertar.html', {'rol': roles})


def listar_usuario(request):
    usuarios = Usuario.objects.all().order_by('last_name')
    total = usuarios.count()
    return render(request, 'usuario/listar.html', {'usuarios': usuarios, 'total_usuarios': total})


def actualizar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        campos = ['tipo_doc', 'numero_documento', 'first_name', 'last_name', 'username', 'email', 'password', 'rol_id']
        if all(request.POST.get(campo) for campo in campos):
            usuario.tipo_doc = request.POST['tipo_doc']
            usuario.numero_documento = request.POST['numero_documento']
            usuario.first_name = request.POST['first_name']
            usuario.last_name = request.POST['last_name']
            usuario.username = request.POST['username']
            usuario.email = request.POST['email']
            usuario.set_password(request.POST['password'])
            usuario.rol_id = request.POST['rol_id']
            usuario.save()
            return redirect('listar_usuario')
    roles = Rol.objects.all()
    return render(request, 'usuario/actualizar.html', {'usuario': usuario, 'rol': roles})


def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect('listar_usuario')

def conteo_usuarios(request):
    total_usuarios = Usuario.objects.count() 
    return render(request, "usuario/listar.html", {})




# Regional


def insertar_regional(request):
    if request.method == 'POST':
        if (request.POST.get('codigo')
            and request.POST.get('nombre')):

                regional = Regional()

                regional.codigo = request.POST.get('codigo')
                regional.nombre = request.POST.get('nombre')
                regional.save()
                return redirect('listar_regional')
    else:
        return render(request, 'regional/insertar.html')
    
def listar_regional (request):
    regional = Regional.objects.all()
    return render(request, 'regional/listar.html', {'regional':regional})

def actualizar_regional(request,id):
    regional=get_object_or_404(Regional,id=id)
    if request.method=='POST':
        campos_obligatorios=['codigo','nombre']

        if all(request.POST.get(field) for field in campos_obligatorios):
            regional.id=id
            regional.codigo=request.POST.get('codigo')
            regional.nombre=request.POST.get('nombre')
            regional.save()
            return redirect('listar_regional')
    else:
        return render(request,'regional/actualizar.html', {'regional':regional})
    
def eliminar_regional(request,id):
    regional=get_object_or_404(Regional,id=id)
    regional.delete() 
    return redirect ('listar_regional')





# Centro_formacion




def insertar_centro_formacion(request):
    if request.method == 'POST':
    
        if (request.POST.get('codigo') 
            and request.POST.get('nombre') 
            and request.POST.get('direccion') 
            and request.POST.get('telefono') 
            and request.POST.get('regional_id')):
            
        
            centro_formacion = CentroFormacion()
                
            centro_formacion.codigo=request.POST.get('codigo')
            centro_formacion.nombre=request.POST.get('nombre')
            centro_formacion.direccion=request.POST.get('direccion')
            centro_formacion.telefono=request.POST.get('telefono')
            centro_formacion.regional_id=request.POST.get('regional_id')
            centro_formacion.save()

            return redirect('listar_centro_formacion')  
            
    else:
        regional = Regional.objects.all()
        return render(request, 'centro_formacion/insertar.html', {'regional': regional})


def listar_centro_formacion(request):
    centro_formacion = CentroFormacion.objects.all()
    regional = Regional.objects.all()
    return render(request,'centro_formacion/listar.html',{'centro_formacion':centro_formacion,'regional':regional})



def actualizar_centro_formacion(request,id):
    centro_formacion=get_object_or_404(CentroFormacion,id=id)
    if request.method=='POST':
        campos_obligatorios=['codigo','nombre','direccion','telefono','regional_id']

        if all(request.POST.get(field) for field in campos_obligatorios):
            centro_formacion.id=id
            centro_formacion.codigo=request.POST.get('codigo')
            centro_formacion.nombre=request.POST.get('nombre')
            centro_formacion.direccion=request.POST.get('direccion')
            centro_formacion.telefono=request.POST.get('telefono')
            centro_formacion.regional_id=request.POST.get('regional_id')
            centro_formacion.save()
            return redirect('listar_centro_formacion')
    else:
        regional = Regional.objects.all()
        return render(request,'centro_formacion/actualizar.html', {'centro_formacion':centro_formacion, 'regional':regional})
    
    
def eliminar_centro_formacion(request, id):
    centro_formacion= get_object_or_404(CentroFormacion,id=id)
    centro_formacion.delete()
    return redirect('listar_centro_formacion')








def insertar_sede(request):
    if request.method == 'POST':
    
        if (request.POST.get('codigo') 
            and request.POST.get('nombre') 
            and request.POST.get('direccion') 
            and request.POST.get('centro_de_formacion_id')):
            
        
            sede = Sede()
                
            sede.codigo=request.POST.get('codigo')
            sede.nombre=request.POST.get('nombre')
            sede.direccion=request.POST.get('direccion')
            sede.centro_de_formacion_id=request.POST.get('centro_de_formacion_id')
            sede.save()

            return redirect('listar_sede')  
            
    else:
        centro_de_formacion = CentroFormacion.objects.all()
        return render(request, 'sede/insertar.html', {'centro_de_formacion': centro_de_formacion})


def listar_sede(request):
    sede = Sede.objects.all()
    centro_de_formacion = CentroFormacion.objects.all()
    return render(request,'sede/listar.html',{'sede':sede,'centro_de_formacion':centro_de_formacion})



def actualizar_sede(request,id):
    sede=get_object_or_404(Sede,id=id)
    if request.method=='POST':
        campos_obligatorios=['codigo','nombre','direccion','centro_de_formacion_id']

        if all(request.POST.get(field) for field in campos_obligatorios):
            sede.id=id
            sede.codigo=request.POST.get('codigo')
            sede.nombre=request.POST.get('nombre')
            sede.direccion=request.POST.get('direccion')
            sede.centro_de_formacion_id=request.POST.get('centro_de_formacion_id')
            sede.save()
            return redirect('listar_sede')
    else:
        centro_de_formacion = CentroFormacion.objects.all()
        return render(request,'sede/actualizar.html', {'sede':sede, 'centro_de_formacion':centro_de_formacion})
    
    
def eliminar_sede(request, id):
    sede= get_object_or_404(Sede,id=id)
    sede.delete()
    return redirect('listar_sede')












def insertar_tipo_ambiente(request):
    if request.method == 'POST':
        if (request.POST.get('codigo')
            and request.POST.get('nombre')):

                tipo_ambiente = TipoAmbiente()

                tipo_ambiente.codigo = request.POST.get('codigo')
                tipo_ambiente.nombre = request.POST.get('nombre')
                tipo_ambiente.save()
                return redirect('listar_tipo_ambiente')
    else:
        return render(request, 'tipo_ambiente/insertar.html')
    
def listar_tipo_ambiente (request):
    tipo_ambiente = TipoAmbiente.objects.all()
    return render(request, 'tipo_ambiente/listar.html', {'tipo_ambiente':tipo_ambiente})

def actualizar_tipo_ambiente(request,id):
    tipo_ambiente=get_object_or_404(TipoAmbiente,id=id)
    if request.method=='POST':
        campos_obligatorios=['codigo','nombre']

        if all(request.POST.get(field) for field in campos_obligatorios):
            tipo_ambiente.id=id
            tipo_ambiente.codigo=request.POST.get('codigo')
            tipo_ambiente.nombre=request.POST.get('nombre')
            tipo_ambiente.save()
            return redirect('listar_tipo_ambiente')
    else:
        return render(request,'tipo_ambiente/actualizar.html', {'tipo_ambiente':tipo_ambiente})
    
def eliminar_tipo_ambiente(request,id):
    tipo_ambiente=get_object_or_404(TipoAmbiente,id=id)
    tipo_ambiente.delete() 
    return redirect ('listar_tipo_ambiente') 










def insertar_ambiente(request):
    if request.method == 'POST':
    
        if (request.POST.get('codigo') 
            and request.POST.get('estado') 
            and request.POST.get('ubicacion')  
            and request.POST.get('tipo_ambiente_id')
            and request.POST.get('sede_id')):
            
        
            ambiente = Ambiente()
                
            ambiente.codigo=request.POST.get('codigo')
            ambiente.estado=request.POST.get('estado')
            ambiente.ubicacion=request.POST.get('ubicacion')
            ambiente.tipo_ambiente_id=request.POST.get('tipo_ambiente_id')
            ambiente.sede_id=request.POST.get('sede_id')
            ambiente.save()

            return redirect('listar_ambiente')  
            
    else:
        tipo_ambiente = TipoAmbiente.objects.all()
        sede = Sede.objects.all()
        return render(request, 'ambiente/insertar.html', {'tipo_ambiente': tipo_ambiente,'sede': sede})


def listar_ambiente(request):
    ambiente = Ambiente.objects.all()
    tipo_ambiente = TipoAmbiente.objects.all()
    sede = Sede.objects.all()
    return render(request,'ambiente/listar.html',{'ambiente':ambiente,'tipo_ambiente':tipo_ambiente,'sede': sede})



def actualizar_ambiente(request,id):
    ambiente=get_object_or_404(Ambiente,id=id)
    if request.method=='POST':
        campos_obligatorios=['codigo','estado','ubicacion','sede_id','tipo_ambiente_id']

        if all(request.POST.get(field) for field in campos_obligatorios):
            ambiente.id=id
            ambiente.codigo=request.POST.get('codigo')
            ambiente.estado=request.POST.get('estado')
            ambiente.ubicacion=request.POST.get('ubicacion')
            ambiente.tipo_ambiente_id=request.POST.get('tipo_ambiente_id')
            ambiente.sede_id=request.POST.get('sede_id')
            ambiente.save()
            return redirect('listar_ambiente')
    else:
        tipo_ambiente = TipoAmbiente.objects.all()
        sede = Sede.objects.all()
        return render(request,'ambiente/actualizar.html', {'ambiente':ambiente, 'tipo_ambiente':tipo_ambiente,'sede': sede})
    
    
def eliminar_ambiente(request, id):
    ambiente= get_object_or_404(Ambiente,id=id)
    ambiente.delete()
    return redirect('listar_ambiente')












def insertar_tipo_mobiliario(request):
    if request.method == 'POST':
        if (request.POST.get('codigo')
            and request.POST.get('descripcion')):

                tipo_mobiliario = TipoMobiliario()

                tipo_mobiliario.codigo = request.POST.get('codigo')
                tipo_mobiliario.descripcion = request.POST.get('descripcion')
                tipo_mobiliario.save()
                return redirect('listar_tipo_mobiliario')
    else:
        return render(request, 'tipo_mobiliario/insertar.html')
    
def listar_tipo_mobiliario (request):
    tipo_mobiliario = TipoMobiliario.objects.all()
    return render(request, 'tipo_mobiliario/listar.html', {'tipo_mobiliario':tipo_mobiliario})

def actualizar_tipo_mobiliario(request,id):
    tipo_mobiliario=get_object_or_404(TipoMobiliario,id=id)
    if request.method=='POST':
        campos_obligatorios=['codigo','descripcion']

        if all(request.POST.get(field) for field in campos_obligatorios):
            tipo_mobiliario.id=id
            tipo_mobiliario.codigo=request.POST.get('codigo')
            tipo_mobiliario.descripcion=request.POST.get('descripcion')
            tipo_mobiliario.save()
            return redirect('listar_tipo_mobiliario')
    else:
        return render(request,'tipo_mobiliario/actualizar.html', {'tipo_mobiliario':tipo_mobiliario})
    
def eliminar_tipo_mobiliario(request,id):
    tipo_mobiliario=get_object_or_404(TipoMobiliario,id=id)
    tipo_mobiliario.delete() 
    return redirect ('listar_tipo_mobiliario') 













def insertar_mobiliario(request):
    if request.method == 'POST':
    
        if (request.POST.get('placa') 
            and request.POST.get('modelo') 
            and request.POST.get('descripcion')
            and request.POST.get('atributos')
            and request.POST.get('observaciones')
            and request.POST.get('fecha_adquisicion')
            and request.POST.get('valor_ingreso')
            and request.POST.get('tipo_id')
            and request.POST.get('ambiente_id')):
            
        
            mobiliario = Mobiliario()
                
            mobiliario.placa=request.POST.get('placa')
            mobiliario.modelo=request.POST.get('modelo')
            mobiliario.descripcion=request.POST.get('descripcion')
            mobiliario.atributos=request.POST.get('atributos')
            mobiliario.observaciones=request.POST.get('observaciones')
            mobiliario.fecha_adquisicion=request.POST.get('fecha_adquisicion')
            mobiliario.valor_ingreso=request.POST.get('valor_ingreso')
            mobiliario.tipo_id=request.POST.get('tipo_id')
            mobiliario.ambiente_id=request.POST.get('ambiente_id')
            mobiliario.save()

            return redirect('listar_mobiliario')  
            
    else:
        tipo_mobiliario = TipoMobiliario.objects.all()
        ambiente = Ambiente.objects.all()
        return render(request, 'mobiliario/insertar.html', {'tipo_mobiliario': tipo_mobiliario,'ambiente': ambiente})


def listar_mobiliario(request):
    mobiliario = Mobiliario.objects.all()
    tipo_mobiliario = TipoMobiliario.objects.all()
    ambiente = Ambiente.objects.all()
    return render(request, 'mobiliario/listar.html', {'mobiliario':mobiliario,'tipo_mobiliario': tipo_mobiliario,'ambiente': ambiente}) 



def actualizar_mobiliario(request,id):
    mobiliario=get_object_or_404(Mobiliario,id=id)
    if request.method=='POST':
        campos_obligatorios=['placa','modelo','descripcion','atributos','observaciones','fecha_adquisicion','valor_ingreso','ambiente_id','tipo_id']

        if all(request.POST.get(field) for field in campos_obligatorios):
            mobiliario.id=id
            mobiliario.placa=request.POST.get('placa')
            mobiliario.modelo=request.POST.get('modelo')
            mobiliario.descripcion=request.POST.get('descripcion')
            mobiliario.atributos=request.POST.get('atributos')
            mobiliario.observaciones=request.POST.get('observaciones')
            mobiliario.fecha_adquisicion=request.POST.get('fecha_adquisicion')
            mobiliario.valor_ingreso=request.POST.get('valor_ingreso')
            mobiliario.tipo_id=request.POST.get('tipo_id')
            mobiliario.ambiente_id=request.POST.get('ambiente_id')
            mobiliario.save()
            return redirect('listar_mobiliario')
    else:
        tipo_mobiliario = TipoMobiliario.objects.all()
        ambiente = Ambiente.objects.all()
        return render(request,'mobiliario/actualizar.html', {'mobiliario':mobiliario, 'tipo_mobiliario':tipo_mobiliario,'ambiente': ambiente})
    
    
def eliminar_mobiliario(request, id):
    mobiliario= get_object_or_404(Mobiliario,id=id)
    mobiliario.delete()
    return redirect('listar_mobiliario')