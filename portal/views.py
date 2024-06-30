from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .models import User, Curso, Periodo, Asignatura, Evaluacion, Asistencia
from .forms import crearCurso, crearPeriodo, crearAsignatura, estudianteCreation, docenteCreation, RICreation
from django.contrib.auth import login as auth_login, logout, authenticate
from django.db import IntegrityError
from datetime import datetime
import locale
import json

locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')


def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request,'index.html')
#-----------------------------
#--------- PERIODO -----------
#-----------------------------

def periodo(request, id_user):
    form = crearPeriodo()
    periodo = Periodo.objects.all()
    if request.method == 'GET':
        return render(request, 'periodo.html',{'form':form, 
                                               'periodo':periodo,
                                               'id':id_user})
    else:
        try:
            form = crearPeriodo(data = request.POST)
            form2 = request.POST.get('predeterminado', 'True')
            nombre1 = request.POST["nombre"]
            if form2 == 'on':
                periodo1 = Periodo.objects.filter(nombre = nombre1).only('predeterminado')
                periodo1 = True
                guardar = Periodo.objects.create(nombre = request.POST["nombre"], 
                                                 fecha_inicio=request.POST["fecha_inicio"],
                                                 fecha_fin=request.POST["fecha_fin"],
                                                 predeterminado = periodo1)
                guardar.save()
                return redirect('periodo',id_user)
            else:
                if form.is_valid():
                    form.save()
                    return redirect('periodo',id_user)
                else:
                    return render(request, 
                                  'periodo.html',
                                  {'form':form, 
                                   'periodo':periodo,
                                   'error':'Solo un Periodo puede ser predeterminado2',
                                   'id':id_user})
        except IntegrityError:
            return render(request, 
                          'periodo.html',
                          {'form':form, 
                           'periodo':periodo,
                           'error':'Solo un Periodo puede ser predeterminado3',
                           'id':id_user})
    
def editarPeriodo(request,id_user, periodo_id):
    if request.method == 'GET':
        periodo = get_object_or_404(Periodo, pk=periodo_id)
        form = crearPeriodo(instance=periodo)
        return render(request, 'editarPeriodo.html', {'periodo':periodo, 
                                                      'form': form,
                                                      'id':id_user})
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
                return redirect('periodo', id_user)
            else:
                periodo = get_object_or_404(Periodo, pk=periodo_id)
                form = crearPeriodo(request.POST, instance=periodo)
                form.save()
                return redirect('periodo', id_user)
        except ValueError:
            return render(request, 'editarPeriodo.html', {'periodo':periodo, 
                                                          'form': form, 
                                                          'error':'Ha ocurrido un error con los parametros ingresados',
                                                          'id':id_user})

def eliminarPeriodo(request,id_user,periodo_id):
    periodo = Periodo.objects.get(pk=periodo_id)
    periodo.delete()
    return redirect('periodo', id_user)

#----------------------------
#--------- CURSOS -----------
#----------------------------

def cursos(request,id_user,id_periodo):
    formularioCurso = crearCurso()
    verCursos = Curso.objects.filter(periodo_id = id_periodo)
    if request.method == 'GET':
        return render(request, 'verCursos.html', {'form': crearCurso, 
                                                  'cursos': verCursos,
                                                  'id':id_user})
    else:
        formularioCurso = crearCurso(data=request.POST)
        if formularioCurso.is_valid():
            curso = Curso.objects.create(nombre = request.POST["nombre"], seccion=request.POST["seccion"],periodo_id = id_periodo)
            curso.save()
            return redirect('cursos',id_user,id_periodo)
        else:
            return redirect('cursos',id_user,id_periodo)
    
def editarCursos(request,id_user,curso_id, id_periodo):
    if request.method == 'GET':
        periodo = Periodo.objects.filter(predeterminado = True)
        curso = get_object_or_404(Curso, pk=curso_id)
        form = crearCurso(instance=curso)
        return render(request, 'editarCursos.html', {'curso':curso, 
                                                     'form': form, 
                                                     'periodo':periodo,
                                                     'id':id_user})
    else:
        try:
            curso = get_object_or_404(Curso, pk=curso_id)
            form = crearCurso(request.POST, instance=curso)
            form.save()
            return redirect('cursos',id_user,id_periodo)
        except ValueError:
            return render(request, 'editarCursos.html', {'curso':curso, 
                                                         'form': form, 
                                                         'error':'Ha ocurrido un error con los parametros ingresados',
                                                         'id':id_user})

def estudiantesCursos (request,id_user,curso_idd):
    obtenerUsuario = User.objects.filter(curso_id = curso_idd)
    estudianteSinCurso = User.objects.filter(curso_id = None, groups__name='Estudiante')
    curso = Curso.objects.get(pk = curso_idd)
    periodo = Periodo.objects.get(predeterminado = True)

    if request.method == 'POST':
        idAgregar = request.POST['estudiante']
        buscarEstudiante = User.objects.get(pk = idAgregar) 
        buscarEstudiante.curso_id = curso.id
        buscarEstudiante.save()
        return redirect('listaEst',id_user,curso_idd)
    
    return render(request, 'listaEst.html',{'usuario':obtenerUsuario,
                                            'id':id_user,
                                            'curso':curso,
                                            'estudianteSolo':estudianteSinCurso,
                                            'periodo':periodo})
    

def eliminarCursos(request,id_user,curso_id, id_periodo):
    curso = Curso.objects.get(pk=curso_id)
    curso.delete()
    return redirect('cursos',id_user,id_periodo)

def eliminarAlumnoCurso(request,id_user,curso_idd,usuario_id):
    obtenerUsuario = User.objects.filter(curso_id = curso_idd).only('id').get(pk=usuario_id)
    if obtenerUsuario.id == usuario_id:
        obtenerUsuario.curso_id = None
        obtenerUsuario.save()
        return redirect('listaEst',id_user,curso_idd)
    else:
        return redirect('listaEst',id_user,curso_idd)
    
#--------------------------------
#--------- ASIGNATURA -----------
#--------------------------------

def asignatura(request,id_user,id_curso):
    form = crearAsignatura()
    verAsignaturas = Asignatura.objects.filter(curso_id = id_curso)
    periodo = Periodo.objects.filter(predeterminado = True)
    if request.method == 'GET':
        return render(request, 'asignatura.html', {'form':form, 
                                                   'asignatura': verAsignaturas,
                                                   'periodo':periodo,
                                                   'id':id_user})
    else:
        try:
            asignatura = Asignatura.objects.create(nombre = request.POST["nombre"], curso_id = id_curso)
            asignatura.save()
            return redirect('asignatura',id_user,id_curso)
        except:
            return render(request,'asignatura.html',id_user,id_curso, {'error':'Algo ha salido mal',
                                                                       'id':id_user})

def editarAsignatura(request,id_user,id_asignatura,id_curso):
    if request.method == 'GET':
        periodo = Periodo.objects.filter(predeterminado = True)
        asignatura = get_object_or_404(Asignatura, pk=id_asignatura)
        form = crearAsignatura(instance=asignatura)
        return render(request, 'editarAsignatura.html', {'asignatura':asignatura, 
                                                         'form': form, 
                                                         'periodo':periodo,
                                                         'id':id_user})
    else:
        try:
            asignatura = get_object_or_404(Asignatura, pk=id_asignatura)
            form = crearAsignatura(request.POST, instance=asignatura)
            form.save()
            return redirect('asignatura',id_user,id_curso)
        except ValueError:
            return render(request, 
                          'asignatura.html',
                          id_curso, 
                          {'curso':asignatura, 
                           'form': form, 
                           'error':'Ha ocurrido un error con los parametros ingresados',
                           'id':id_user})
        
def eliminarAsignatura(request,id_user,id_asignatura,id_curso):
    asignatura = Asignatura.objects.get(pk=id_asignatura)
    asignatura.delete()
    return redirect('asignatura',id_user,id_curso)

#--------------------------------
#--------- NOTAS ----------------
#--------------------------------

def alumnosNotas(request,id_user,id_curso, asgn_id):
    periodo = Periodo.objects.get(predeterminado=True)
    verAsignaturas = get_object_or_404(Asignatura, curso_id=id_curso, pk=asgn_id)
    estudiantes = User.objects.filter(curso_id=id_curso)
    promedios = calcularPromedios(estudiantes, verAsignaturas.id, id_curso, periodo.id)
    notirijillas = obtenerNotas(estudiantes, verAsignaturas.id, id_curso, periodo.id)
    if request.method == 'GET':
        return render(request, 'alumnosAsignaturas.html', {
            'asignatura': verAsignaturas,
            'estudiante': estudiantes,
            'periodo': periodo,
            'promedios': promedios,
            'notas':notirijillas,
            'id':id_user
        })

    try:
        nota = int(request.POST["nota"])
        if nota > 70 or nota < 10:
            raise ValueError("Nota fuera de rango")
    except (ValueError, TypeError):
        return render(request, 'alumnosAsignaturas.html', {
            'asignatura': verAsignaturas,
            'estudiante': estudiantes,
            'periodo': periodo,
            'promedios': promedios,
            'notas':notirijillas,
            'error': 'Ingrese un número válido',
            'id':id_user
        })

    evaluacion, created = Evaluacion.objects.get_or_create(
        usuario_id=request.POST["id"],
        asignatura_id=verAsignaturas.id,
        curso_id=id_curso,
        periodo_id=periodo.id,
        defaults={'nota1': nota,}
    )

    if not created:
        notas = ['nota2', 'nota3', 'nota4', 'nota5', 'nota6', 'nota7', 'nota8', 'nota9']
        for field in notas:
            if getattr(evaluacion, field) is None:
                setattr(evaluacion, field, nota)
                evaluacion.save()
                return redirect('alumnosNotas',id_user,id_curso, asgn_id)
        return render(request, 'alumnosAsignaturas.html', {
            'asignatura': verAsignaturas,
            'estudiante': estudiantes,
            'periodo': periodo,
            'promedios': promedios,
            'notas':notirijillas,
            'error': 'Todas las notas están completas',
            'id':id_user
        })
        

    return redirect('alumnosNotas',id_user,id_curso, asgn_id)

def calcularPromedios(estudiantes, asignatura_id, curso_id, periodo_id):
    promedios = {}
    for estudiante in estudiantes:
        evaluaciones = Evaluacion.objects.filter(
            usuario_id=estudiante.id,
            asignatura_id=asignatura_id,
            curso_id=curso_id,
            periodo_id=periodo_id
        )
        notas = []
        for evaluacion in evaluaciones:
            notas.extend([
                evaluacion.nota1, evaluacion.nota2, evaluacion.nota3, evaluacion.nota4,
                evaluacion.nota5, evaluacion.nota6, evaluacion.nota7, evaluacion.nota8,
                evaluacion.nota9
            ])
        notas = [nota for nota in notas if nota is not None]
        if notas:
            promedio = round(sum(notas) / len(notas))
            promedios[estudiante.id] = promedio
            for evaluacion in evaluaciones:
                evaluacion.promedio = promedio
                evaluacion.save()
        else:
            promedios[estudiante.id] = None
    return promedios

def obtenerNotas(estudiantes, asignatura_id, curso_id, periodo_id):
    notasEst = {}
    for estudiante in estudiantes:
        evaluaciones = Evaluacion.objects.filter(
            usuario_id=estudiante.id,
            asignatura_id=asignatura_id,
            curso_id=curso_id,
            periodo_id=periodo_id
        )
        notas = []
        for evaluacion in evaluaciones:
            notas.extend([
                evaluacion.nota1, evaluacion.nota2, evaluacion.nota3, evaluacion.nota4,
                evaluacion.nota5, evaluacion.nota6, evaluacion.nota7, evaluacion.nota8,
                evaluacion.nota9
            ])
        notas = [nota for nota in notas if nota is not None]
        if notas:
            notasEst[estudiante.id] = notas
        else:
            notasEst[estudiante.id] = None
    return notasEst
#--------------------------------------
#--------- LOGIN Y REGISTRO -----------
#--------------------------------------

def signupEstudiante(request,id_user):
    if request.method == 'GET':
        idPeriodoSet = Periodo.objects.filter(predeterminado = True).values('id')
        curso = Curso.objects.filter(periodo_id=idPeriodoSet[0]['id'])
        return render(request, 'signupEstudiante.html', {"form": estudianteCreation,
                                                         "curso":curso,
                                                         'id':id_user})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                año = datetime.strptime(request.POST["fecha_nacimiento"] , '%Y-%m-%d')
                estudiante = Group.objects.filter(name = "Estudiante").values("id")
                username = request.POST["first_name"][:2]+'.'+request.POST["last_name"]+'E'
                age = datetime.now().year - año.year
                print(username)
                user = User.objects.create_user( username = username, 
                                                password=request.POST["password1"],
                                                edad = age, 
                                                curso_id=request.POST["curso"], 
                                                first_name = request.POST["first_name"],
                                                email = request.POST["email"], 
                                                last_name = request.POST ["last_name"], 
                                                telefono = request.POST["telefono"],
                                                imagenPerfil = request.POST["imagenPerfil"], 
                                                direccion = request.POST["direccion"],
                                                fecha_nacimiento = request.POST["fecha_nacimiento"], 
                                                groups_id = estudiante)
                user.save()
                return redirect('perfil_ri',id_user)
            except IntegrityError:
                return render(request, 'signupEstudiante.html', {"form": estudianteCreation, 
                                                                 "error": "Este nombre de usuario ya existe.",
                                                                 'id':id_user})

        return render(request, 'signupEstudiante.html', {"form": estudianteCreation, 
                                                         "error": "La contraseña no coincide",
                                                         'id':id_user})
    
def signupDocente(request,id_user):
    if request.method == 'GET':
        idPeriodoSet = Periodo.objects.filter(predeterminado = True).values('id')
        curso = Curso.objects.filter(periodo_id=idPeriodoSet[0]['id'])
        return render(request, 'signupDocente.html', {"form": docenteCreation,
                                                      "curso":curso,
                                                      'id':id_user})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                año = datetime.strptime(request.POST["fecha_nacimiento"] , '%Y-%m-%d')
                docente = Group.objects.filter(name = "Docente").values("id")
                username = request.POST["first_name"][:2]+'.'+request.POST["last_name"]+'D'
                age = datetime.now().year - año.year
                user = User.objects.create_user(username = username, 
                                                password=request.POST["password1"],
                                                edad = age,
                                                first_name = request.POST["first_name"], 
                                                last_name = request.POST ["last_name"],
                                                email = request.POST["email"], 
                                                telefono = request.POST["telefono"],
                                                imagenPerfil = request.POST["imagenPerfil"], 
                                                direccion = request.POST["direccion"],
                                                fecha_nacimiento = request.POST["fecha_nacimiento"],
                                                curso_id = request.POST["curso"],
                                                groups_id = docente)
                user.save()
                return redirect('perfil_ri',id_user)
            except IntegrityError:
                return render(request, 'signupDocente.html', {"form": docenteCreation, 
                                                              "error": "Este nombre de usuario ya existe.",
                                                              'id':id_user})

        return render(request, 'signupDocente.html', {"form": docenteCreation, 
                                                      "error": "La contraseña no coincide",
                                                      'id':id_user}) 
    
def signupRI(request,id_user):
    if request.method == 'GET':
        return render(request, 'signupRI.html', {"form": RICreation,
                                                 'id':id_user})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                año = datetime.strptime(request.POST["fecha_nacimiento"] , '%Y-%m-%d')
                ri = Group.objects.filter(name = "Responsable Institucional").values("id")
                username = request.POST["first_name"][:2]+'.'+request.POST["last_name"]+'RI'
                age = datetime.now().year - año.year
                user = User.objects.create_user( username = username, 
                                                password=request.POST["password1"],
                                                edad = age,
                                                first_name = request.POST["first_name"], 
                                                last_name = request.POST ["last_name"],
                                                email = request.POST["email"],
                                                telefono = request.POST["telefono"],
                                                direccion = request.POST["direccion"],
                                                fecha_nacimiento = request.POST["fecha_nacimiento"],
                                                groups_id = ri)
                user.save()
                return redirect('perfil_ri',id_user)
            except IntegrityError:
                return render(request, 'signupRI.html', {"form": RICreation, 
                                                         "error": "Este nombre de usuario ya existe.",
                                                         'id':id_user})

        return render(request, 'signupRI.html', {"form": RICreation, 
                                                 "error": "La contraseña no coincide",
                                                 'id':id_user}) 
    
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
        username2 = request.POST['username']
        password2 = request.POST['password']
        id_usuario = User.objects.get(username = username2)
        
        user = authenticate(
            request, username=username2, password=password2)
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "El usuario o la contraseña son incorrectos."})
        else:
            if user in estudiante:  
                auth_login(request, user)
                return redirect('perfil', id_usuario.id)
            elif user in ri or docente:  
                auth_login(request, user)
                return redirect('perfil_ri', id_usuario.id)
            else:
                return render(request, 'signin.html',{"error":"ha ocurrido un error"})

#--------------------------------
#--------- ASISTENCIA -----------
#--------------------------------
def listaCurso(request,id_user,id_periodo):
    curso = Curso.objects.filter(periodo_id = id_periodo)
    return render(request,'asistenciaselectCurso.html',{'cursos':curso,
                                                        'id':id_user})

def asistenciasCurso(request,id_user, id_periodo,id_curso):
    fechas = Asistencia.objects.filter(curso_id = id_curso).values_list('fecha',flat=True).distinct()
    if fechas.exists():
        fechaUltimate = []
        for fecha in fechas:
            fecha2 = datetime.strftime(fecha,'%d %B, %Y')
            fechaUltimate.append(fecha2)
    else:
        fechaUltimate = None
    curso = Curso.objects.get(id = id_curso)
    return render(request,'asistenciasCurso.html',{'fechas':fechaUltimate,
                                                   'curso':curso,
                                                   'periodo':id_periodo,
                                                   'id':id_user})

def eliminarAsistencia(request,id_user, fecha_asistencia):
    periodo = Periodo.objects.get(predeterminado=True)
    fecha5 = datetime.strptime(fecha_asistencia, '%d %B, %Y').date()
    fecha = Asistencia.objects.filter(fecha = fecha5, periodo_id = periodo.id)
    fechaAborrar = Asistencia.objects.filter(fecha = fecha5).values('curso_id')
    id_curso = fechaAborrar[0]['curso_id']
    fecha.delete()
    return redirect('asistenciasCurso',id_user,periodo.id,id_curso)

def listaAsistencia(request,id_user, id_curso, fecha_asistencia):
    curso = Curso.objects.get(pk = id_curso)
    periodo = Periodo.objects.get(predeterminado=True)
    fecha5 = datetime.strptime(fecha_asistencia, '%d %B, %Y').date()
    asistencia_existente = Asistencia.objects.filter(fecha = fecha5, curso_id = id_curso)
    getEstudiantes = Asistencia.objects.filter(fecha = fecha5, curso_id = id_curso).values_list('usuario_id',flat=True)
    est = User.objects.filter(id__in = getEstudiantes)
    
    if request.method == 'POST':
        for asistencia in asistencia_existente:
            asistio = request.POST.get(f'asistio_{asistencia.usuario.id}', 'off') == 'on'
            asistencia.asistio = asistio
            asistencia.save()

        return redirect('asistenciasCurso',id_user, periodo.id, curso.id ) 
    
    return render(request, 'listaAsistencia.html', {'estudiantes':est,
                                                     'periodo':periodo, 
                                                     'fechaMostrable': fecha_asistencia,
                                                     'curso':curso,
                                                     'asistencia_existente':asistencia_existente,
                                                     'periodo': periodo,
                                                     'id':id_user})

def registrarAsistencia(request,id_user,id_periodo,id_curso):
    estudiantes = User.objects.filter(curso_id = id_curso ,groups__name='Estudiante')
    curso = Curso.objects.get(pk=id_curso)
    if request.method == 'GET':
        if Asistencia.objects.filter(fecha = datetime.now().date(),curso_id = id_curso).exists():
            print("error")
            return redirect('asistenciasCurso',id_user,id_periodo,id_curso)
        else:
            fecha = datetime.strftime(datetime.now(),'%d %B, %Y')
            return render(request, 'registrarAsistencia.html', {'estudiantes': estudiantes, 
                                                                'fecha':fecha, 
                                                                'curso':curso, 
                                                                'periodo':id_periodo,
                                                                'id':id_user})
    else:
        for estudiante in estudiantes:
            asistio = request.POST.get(f'asistio_{estudiante.id}', 'off') == 'on'
            #fecha_custom = '11-05-2024'
            Asistencia.objects.create(
                fecha=datetime.now().date(),
                #fecha = datetime.strptime(fecha_custom,'%d-%m-%Y').date(),
                usuario_id=estudiante.id,
                curso_id = id_curso,
                periodo_id = id_periodo,
                asistio=asistio
        )
        return redirect('asistenciasCurso',id_user,id_periodo,id_curso)

            
#------------------------------
#--------- PERFILES -----------
#------------------------------

def mostrarNotas(estudiantes_id, asignaturas, curso_id, periodo_id):
    notasEst = {}
    for asignatura in asignaturas:
        evaluaciones = Evaluacion.objects.filter(
            usuario_id=estudiantes_id,
            asignatura_id=asignatura.id,
            curso_id=curso_id,
            periodo_id=periodo_id
        )
        notas = []
        for evaluacion in evaluaciones:
            notas.extend([
                evaluacion.nota1, evaluacion.nota2, evaluacion.nota3, evaluacion.nota4,
                evaluacion.nota5, evaluacion.nota6, evaluacion.nota7, evaluacion.nota8,
                evaluacion.nota9
            ])
        notas = [nota for nota in notas if nota is not None]
        if notas:
            notasEst[asignatura.id] = notas
        else:
            notasEst[asignatura.id] = None
    return notasEst

def mostrarPromedios(estudiantes_id, asignaturas, curso_id, periodo_id):
    estProm = {}
    for asignatura in asignaturas:
        evaluaciones = Evaluacion.objects.filter(
            usuario_id=estudiantes_id,
            asignatura_id=asignatura.id,
            curso_id=curso_id,
            periodo_id=periodo_id
        )
        promedios = []
        for evaluacion in evaluaciones:
            promedios.extend([
                evaluacion.promedio
            ])
        promedios = [promedio for promedio in promedios if promedio is not None]
        if promedios:
            estProm[asignatura.id] = promedios
        else:
            estProm[asignatura.id] = None
    return estProm

def promedioGeneral(estudiantes_id, asignaturas, curso_id, periodo_id):
    total_promedios = []

    for asignatura in asignaturas:
        evaluaciones = Evaluacion.objects.filter(
            usuario_id=estudiantes_id,
            asignatura_id=asignatura.id,
            curso_id=curso_id,
            periodo_id=periodo_id
        )
        promedios = [evaluacion.promedio for evaluacion in evaluaciones if evaluacion.promedio is not None]
        if promedios:
            promedio_asignatura = round(sum(promedios) / len(promedios))
            total_promedios.append(promedio_asignatura)
        else:
            pass

    if total_promedios:
        promedio_global = round(sum(total_promedios) / len(total_promedios))
    else:
        promedio_global = None
    return promedio_global

def perfil(request, id_estudiante):
    periodo = Periodo.objects.get(predeterminado=True)
    estudiante = User.objects.get(pk=id_estudiante)
    curso = Curso.objects.get(pk = estudiante.curso_id)
    asignaturas = Asignatura.objects.filter(curso_id = curso.id)
    notas = mostrarNotas(estudiante.id, asignaturas, curso.id, periodo.id)
    promedio = mostrarPromedios(estudiante.id, asignaturas, curso.id, periodo.id)
    promedio_global = promedioGeneral(estudiante.id, asignaturas, curso.id, periodo.id)
    promedio_globalConComilla = str(promedio_global)[:1] + "," + str(promedio_global)[1:2]
    return render(request,
                  'perfil.html',
                  {'estudiante':estudiante,
                    'curso':curso, 
                    'asignaturas': asignaturas,
                    'notas': notas,
                    'promedios':promedio,
                    'promedioGeneral':promedio_globalConComilla
                    })

def asistencia(request, id_estudiante):
    estudiante = User.objects.get(pk = id_estudiante)
    curso = Curso.objects.get(pk = estudiante.curso_id)
    getAsistencias = Asistencia.objects.filter(usuario_id = estudiante.id, curso_id = curso.id).values_list('fecha',flat=True).distinct()
    getAsistenciasAsistidas = Asistencia.objects.filter(usuario_id = estudiante.id, asistio = 1, curso_id = curso.id).values_list('fecha',flat=True).distinct()
    if getAsistencias.exists():
        asistencias = getAsistencias.count()
        asistio = getAsistenciasAsistidas.count()
        porcentajeAsistencia = round((100 * asistio) / asistencias, 1)
        inasistencias = asistencias - asistio
    else:
        asistencias = 0
        asistio = 0
        porcentajeAsistencia = 0
        inasistencias = 0
    return render(request, 'asistencia.html',{'estudiante':estudiante,
                                              'curso':curso,
                                              'asistencias':asistencias,
                                              'asistio':asistio,
                                              'porcentaje':porcentajeAsistencia,
                                              'inasistencias':inasistencias})

def perfilDocente(request):
    return render(request,'perfilDocente.html')

def perfil_ri(request, id_user):
    periodo = Periodo.objects.filter(predeterminado = True)
    return render(request,'perfil_ri.html',{'periodo':periodo,
                                            'id':id_user})
    
