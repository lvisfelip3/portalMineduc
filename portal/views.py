from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .models import User, Curso, Periodo, Asignatura
from .forms import crearCurso, crearPeriodo, crearAsignatura, estudianteCreation, docenteCreation, RICreation
from django.contrib.auth import login as auth_login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponse
from datetime import datetime


def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request,'index.html')

#------------------------------
#--------- PERFILES -----------
#------------------------------

def perfil(request):
    return render(request,'perfil.html')

def perfilDocente(request):
    return render(request,'perfilDocente.html')

def perfil_ri(request):
    periodo = Periodo.objects.filter(predeterminado = True)
    return render(request,'perfil_ri.html',{'periodo':periodo})

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
            form = crearPeriodo(data = request.POST)
            form2 = request.POST.get('predeterminado', 'True')
            nombre1 = request.POST["nombre"]
            if form2 == 'on':
                periodo1 = Periodo.objects.filter(nombre = nombre1).only('predeterminado')
                periodo1 = True
                guardar = Periodo.objects.create(nombre = request.POST["nombre"], fecha_inicio=request.POST["fecha_inicio"],fecha_fin=request.POST["fecha_fin"],predeterminado = periodo1)
                guardar.save()
                return redirect('periodo')
            else:
                if form.is_valid():
                    form.save()
                    return redirect('periodo')
                else:
                    return render(request, 'periodo.html',{'form':form, 'periodo':periodo,'error':'Solo un Periodo puede ser predeterminado2'})
        except IntegrityError:
            return render(request, 'periodo.html',{'form':form, 'periodo':periodo,'error':'Solo un Periodo puede ser predeterminado3'})
    
def editarPeriodo(request, periodo_id):
    if request.method == 'GET':
        periodo = get_object_or_404(Periodo, pk=periodo_id)
        form = crearPeriodo(instance=periodo)
        return render(request, 'editarPeriodo.html', {'periodo':periodo, 'form': form})
    else:
        try:
            predOn = request.POST.get('predeterminado', 'True')
            if predOn == 'on':
                pred = Periodo.objects.get(pk=periodo_id)
                pred.predeterminado = True
                pred.save()
                periodo = get_object_or_404(Periodo, pk=periodo_id)
                form = crearPeriodo(request.POST, instance=periodo)
                form.save()
                return redirect('periodo')
            else:
                periodo = get_object_or_404(Periodo, pk=periodo_id)
                form = crearPeriodo(request.POST, instance=periodo)
                form.save()
                return redirect('periodo')
        except ValueError:
            return render(request, 'editarPeriodo.html', {'periodo':periodo, 'form': form, 'error':'Ha ocurrido un error con los parametros ingresados'})

def eliminarPeriodo(request,periodo_id):
    periodo = Periodo.objects.get(pk=periodo_id)
    periodo.delete()
    return redirect('periodo')

#----------------------------
#--------- CURSOS -----------
#----------------------------

def cursos(request, id_periodo):
    formularioCurso = crearCurso()
    verCursos = Curso.objects.filter(periodo_id = id_periodo)
    if request.method == 'GET':
        return render(request, 'verCursos.html', {'form': crearCurso, 'cursos': verCursos})
    else:
        formularioCurso = crearCurso(data=request.POST)
        if formularioCurso.is_valid():
            curso = Curso.objects.create(nombre = request.POST["nombre"], seccion=request.POST["seccion"],periodo_id = id_periodo)
            curso.save()
            return redirect('cursos',id_periodo)
        else:
            return redirect('cursos',id_periodo, {'error': 'Ha ocurrido un error en la creación de Curso'})
    
def editarCursos(request, curso_id, id_periodo):
    if request.method == 'GET':
        periodo = Periodo.objects.filter(predeterminado = True)
        curso = get_object_or_404(Curso, pk=curso_id)
        form = crearCurso(instance=curso)
        return render(request, 'editarCursos.html', {'curso':curso, 'form': form, 'periodo':periodo})
    else:
        try:
            curso = get_object_or_404(Curso, pk=curso_id)
            form = crearCurso(request.POST, instance=curso)
            form.save()
            return redirect('cursos',id_periodo)
        except ValueError:
            return render(request, 'editarCursos.html', {'curso':curso, 'form': form, 'error':'Ha ocurrido un error con los parametros ingresados'})

def estudiantesCursos (request, curso_idd):
    obtenerUsuario = User.objects.filter(curso_id = curso_idd)
    
    return render(request, 'listaEst.html',{'usuario':obtenerUsuario})
    

def eliminarCursos(request,curso_id, id_periodo):
    curso = Curso.objects.get(pk=curso_id)
    curso.delete()
    return redirect('cursos', id_periodo)

def eliminarAlumnoCurso(request,curso_idd,usuario_id):
    obtenerUsuario = User.objects.filter(curso_id = curso_idd).only('id').get(pk=usuario_id)
    if obtenerUsuario.id == usuario_id:
        obtenerUsuario.curso_id = None
        obtenerUsuario.save()
        return redirect('listaEst',curso_idd)
    else:
        print("algo salio mal")
        return redirect('listaEst', curso_idd)
    
#--------------------------------
#--------- ASIGNATURA -----------
#--------------------------------

def asignatura(request, id_curso):
    form = crearAsignatura()
    verAsignaturas = Asignatura.objects.filter(curso_id = id_curso)
    periodo = Periodo.objects.filter(predeterminado = True)
    if request.method == 'GET':
        return render(request, 'asignatura.html', {'form':form, 'asignatura': verAsignaturas,'periodo':periodo})
    else:
        try:
            asignatura = Asignatura.objects.create(nombre = request.POST["nombre"], curso_id = id_curso)
            asignatura.save()
            return redirect('asignatura',id_curso)
        except:
            return render(request,'asignatura.html',id_curso, {'error':'Algo ha salido mal'})

def editarAsignatura(request, id_asignatura,id_curso):
    if request.method == 'GET':
        periodo = Periodo.objects.filter(predeterminado = True)
        asignatura = get_object_or_404(Asignatura, pk=id_asignatura)
        form = crearAsignatura(instance=asignatura)
        return render(request, 'editarAsignatura.html', {'asignatura':asignatura, 'form': form, 'periodo':periodo})
    else:
        try:
            asignatura = get_object_or_404(Asignatura, pk=id_asignatura)
            form = crearAsignatura(request.POST, instance=asignatura)
            form.save()
            return redirect('asignatura',id_curso)
        except ValueError:
            return render(request, 'asignatura.html',id_curso, {'curso':asignatura, 'form': form, 'error':'Ha ocurrido un error con los parametros ingresados'})
        
def eliminarAsignatura(request,id_asignatura,id_curso):
    asignatura = Asignatura.objects.get(pk=id_asignatura)
    asignatura.delete()
    return redirect('asignatura', id_curso)

#--------------------------------------
#--------- LOGIN Y REGISTRO -----------
#--------------------------------------

def signupEstudiante(request):
    if request.method == 'GET':
        idPeriodoSet = Periodo.objects.filter(predeterminado = True).values('id')
        curso = Curso.objects.filter(periodo_id=idPeriodoSet[0]['id'])
        return render(request, 'signupEstudiante.html', {"form": estudianteCreation,"curso":curso})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                año = datetime.strptime(request.POST["fecha_nacimiento"] , '%Y-%m-%d')
                estudiante = Group.objects.filter(name = "Estudiante").values("id")
                username = request.POST["first_name"][:2]+'.'+request.POST["last_name"]+'E'
                age = datetime.now().year - año.year
                print(username)
                user = User.objects.create_user( username = username, password=request.POST["password1"],edad = age, curso_id=request.POST["curso"], first_name = request.POST["first_name"],email = request.POST["email"], last_name = request.POST ["last_name"], telefono = request.POST["telefono"],imagenPerfil = request.POST["imagenPerfil"], direccion = request.POST["direccion"],fecha_nacimiento = request.POST["fecha_nacimiento"], groups_id = estudiante)
                user.save()
                return redirect('perfil_ri')
            except IntegrityError:
                return render(request, 'signupEstudiante.html', {"form": estudianteCreation, "error": "Este nombre de usuario ya existe."})

        return render(request, 'signupEstudiante.html', {"form": estudianteCreation, "error": "La contraseña no coincide"})
    
def signupDocente(request):
    if request.method == 'GET':
        idPeriodoSet = Periodo.objects.filter(predeterminado = True).values('id')
        curso = Curso.objects.filter(periodo_id=idPeriodoSet[0]['id'])
        return render(request, 'signupDocente.html', {"form": docenteCreation,"curso":curso})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                año = datetime.strptime(request.POST["fecha_nacimiento"] , '%Y-%m-%d')
                docente = Group.objects.filter(name = "Docente").values("id")
                username = request.POST["first_name"][:2]+'.'+request.POST["last_name"]+'D'
                age = datetime.now().year - año.year
                user = User.objects.create_user(username = username, password=request.POST["password1"],edad = age,first_name = request.POST["first_name"], last_name = request.POST ["last_name"],email = request.POST["email"], telefono = request.POST["telefono"],imagenPerfil = request.POST["imagenPerfil"], direccion = request.POST["direccion"],fecha_nacimiento = request.POST["fecha_nacimiento"],curso_id = request.POST["curso"],groups_id = docente)
                user.save()
                return redirect('perfil_ri')
            except IntegrityError:
                return render(request, 'signupDocente.html', {"form": docenteCreation, "error": "Este nombre de usuario ya existe."})

        return render(request, 'signupDocente.html', {"form": docenteCreation, "error": "La contraseña no coincide"}) 
    
def signupRI(request):
    if request.method == 'GET':
        return render(request, 'signupRI.html', {"form": RICreation})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                año = datetime.strptime(request.POST["fecha_nacimiento"] , '%Y-%m-%d')
                ri = Group.objects.filter(name = "Responsable Institucional").values("id")
                username = request.POST["first_name"][:2]+'.'+request.POST["last_name"]+'RI'
                age = datetime.now().year - año.year
                user = User.objects.create_user( username = username, password=request.POST["password1"],edad = age,first_name = request.POST["first_name"], last_name = request.POST ["last_name"],email = request.POST["email"],telefono = request.POST["telefono"],direccion = request.POST["direccion"],fecha_nacimiento = request.POST["fecha_nacimiento"],groups_id = ri)
                user.save()
                return redirect('perfil_ri')
            except IntegrityError:
                return render(request, 'signupRI.html', {"form": RICreation, "error": "Este nombre de usuario ya existe."})

        return render(request, 'signupRI.html', {"form": RICreation, "error": "La contraseña no coincide"}) 
    
def signout(request):
    logout(request)
    return redirect('index')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html' , { 'form': AuthenticationForm})
    else:
        estudiante = Group.objects.get(name="Estudiante").user_set.all()
        docente = Group.objects.get(name="Docente").user_set.all()
        ri = Group.objects.get(name="Responsable Institucional").user_set.all()
        
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "El usuario o la contraseña son incorrectos."})
        else:
            if user in estudiante:  
                auth_login(request, user)
                return redirect('perfil')
            elif user in docente:  
                auth_login(request, user)
                return redirect('perfilDocente')
            elif user in ri:  
                auth_login(request, user)
                return redirect('perfil_ri')
            else:
                return render(request, 'signin.html',{"error":"ha ocurrido un error"})
    
