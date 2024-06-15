from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .models import User, Curso, Periodo
from .forms import crearCurso, CustomUserCreation, crearPeriodo
from django.contrib.auth import login as auth_login, logout, authenticate
from django.db import IntegrityError


def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request,'index.html')

#------------------------------
#--------- PERFILES -----------
#------------------------------

def perfil(request):
    return render(request,'perfil.html')

def perfil_ri(request):
    return render(request,'perfil_ri.html')

#----------------------------
#--------- CURSOS -----------
#----------------------------
def cursos(request):
    formularioCurso = crearCurso()
    verCursos = Curso.objects.all()
    
    if request.method == 'GET':
        return render(request, 'verCursos.html', {'form': crearCurso, 'cursos': verCursos})
    else:
        formularioCurso = crearCurso(data=request.POST)
        if formularioCurso.is_valid():
            formularioCurso.save()
            return redirect('cursos')
        else:
            return redirect('cursos', {'error': 'Ha ocurrido un error en la creación de Curso'})

def editarCursos(request, curso_id):
    if request.method == 'GET':
        curso = get_object_or_404(Curso, pk=curso_id)
        form = crearCurso(instance=curso)
        return render(request, 'editarCursos.html', {'curso':curso, 'form': form})
    else:
        try:
            curso = get_object_or_404(Curso, pk=curso_id)
            form = crearCurso(request.POST, instance=curso)
            form.save()
            return redirect('cursos')
        except ValueError:
            return render(request, 'editarCursos.html', {'curso':curso, 'form': form, 'error':'Ha ocurrido un error con los parametros ingresados'})

def estudiantesCursos (request, curso_idd):
    obtenerUsuario = User.objects.filter(curso_id = curso_idd)
    
    return render(request, 'listaEst.html',{'usuario':obtenerUsuario})
    

def eliminarCursos(request,curso_id):
    curso = Curso.objects.get(pk=curso_id)
    curso.delete()
    return redirect('cursos')

def eliminarAlumnoCurso(request,curso_idd,usuario_id):
    obtenerUsuario = User.objects.filter(curso_id = curso_idd).only('id').get(pk=usuario_id)
    if obtenerUsuario.id == usuario_id:
        obtenerUsuario.curso_id = None
        obtenerUsuario.save()
        return redirect('listaEst',curso_idd)
    else:
        print("algo salio mal")
        return redirect('listaEst', curso_idd)

#-----------------------------
#--------- PERIODO -----------
#-----------------------------
def periodo(request):
    form = crearPeriodo()
    periodo = Periodo.objects.all()
    if request.method == 'GET':
        return render(request, 'periodo.html',{'form':form, 'periodo':periodo})
    else:
        try:
            form = crearPeriodo(request.POST)
            form2 = request.POST["predeterminado"]
            if form2 == 'on':
                periodo1 = Periodo.objects.get(nombre = request.POST["nombre"]).only('predeterminado')
                periodo1 = True
                periodo1.save()
                if form.is_valid():
                    form.save()
                    return redirect('periodo')
                else:
                    return render(request, 'periodo.html',{'form':form, 'periodo':periodo,'error':'Solo un Periodo puede ser predeterminado'})
            else:
                print("vamos mal")
                if form.is_valid():
                    form.save()
                    return redirect('periodo')
                else:
                    return render(request, 'periodo.html',{'form':form, 'periodo':periodo,'error':'Solo un Periodo puede ser predeterminado2'})
        except IntegrityError:
            print(form)
            return render(request, 'periodo.html',{'form':form, 'periodo':periodo,'error':'Solo un Periodo puede ser predeterminado3'})
#--------------------------------------
#--------- LOGIN Y REGISTRO -----------
#--------------------------------------
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": CustomUserCreation})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user( username = request.POST["username"], password=request.POST["password1"], curso_id=request.POST["curso"], first_name = request.POST["first_name"], last_name = request.POST ["last_name"], telefono = request.POST["telefono"],groups_id = request.POST["Usuario"])
                user.save()
                return redirect('perfil_ri')
            except IntegrityError:
                return render(request, 'signup.html', {"form": CustomUserCreation, "error": "Este nombre de usuario ya existe."})

        return render(request, 'signup.html', {"form": CustomUserCreation, "error": "La contraseña no coincide"}) 
    
def signout(request):
    logout(request)
    return redirect('index')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html' , { 'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "El usuario o la contraseña son incorrectos."})
        else:
            auth_login(request, user)
            return redirect('perfil')
    
