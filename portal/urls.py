from django.urls import path
from . import  views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    #-------------------------------------------
    #--------------- BACKEND -------------------
    #-------------------------------------------
    path('IniciarSesion/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    #----------------------------------------------
    #--------------- ESTUDIANTE -------------------
    #----------------------------------------------
    path('Estudiante<int:id_estudiante>/Notas', views.perfil, name="perfil"),
    path('Estudiante<int:id_estudiante>/Asistencia', views.asistencia, name="Easistencia"),
    #-------------------------------------------
    #--------------- DOCENTE -------------------
    #-------------------------------------------
    path('Docente/', views.perfilDocente, name="perfilDocente"),
    #-----------------------------------------
    #--------------- ADMIN -------------------
    #-----------------------------------------
    path('RI/', views.perfil_ri, name="perfil_ri"),

    path('RI/CrearUsuario/Estudiante', views.signupEstudiante, name="signupEstudiante"),
    path('RI/CrearUsuario/Docente', views.signupDocente, name="signupDocente"),
    path('RI/CrearUsuario/RI', views.signupRI, name="signupRI"),

    path('Ri/Periodo<int:id_periodo>/Curso<int:id_curso>/Asistencia', views.asistenciasCurso, name='asistenciasCurso'),
    path('Ri/Curso<str:fecha_asistencia>/Asistencia/delete', views.eliminarAsistencia, name='eliminarAsistencia'),
    path('Ri/Periodo<int:id_periodo>/CursosAsistencia/', views.listaCurso, name='listaCursos'),
    path('Ri/Periodo<int:id_periodo>/Curso<int:id_curso>/RegistroAsistencia', views.registrarAsistencia, name = "asistencia"),
    path('Ri/Curso<int:id_curso>/<str:fecha_asistencia>/RegistroAsistencia', views.listaAsistencia, name = "listaAsistencia"),

    path('Ri/Periodo<int:id_periodo>/Cursos/', views.cursos, name='cursos'),
    path('Ri/Cursos/Curso<int:curso_id>/Periodo<int:id_periodo>', views.editarCursos, name='editarCursos'),
    path('Ri/Cursos/Curso<int:curso_id>/Periodo<int:id_periodo>/delete', views.eliminarCursos, name='eliminarCursos'),

    path('Ri/Cursos/Lista/Curso<int:curso_idd>', views.estudiantesCursos, name="listaEst"),
    path('Ri/Cursos/delete/Curso<int:curso_idd>/Usuario<int:usuario_id>', views.eliminarAlumnoCurso, name="eliminarAlumnoCurso"),

    path('Ri/Periodo', views.periodo, name = "periodo"),
    path('Ri/editarPeriodo/Periodo<int:periodo_id>', views.editarPeriodo, name = "editarPeriodo"),
    path('Ri/editarPeriodo/Periodo<int:periodo_id>/delete', views.eliminarPeriodo, name = "eliminarPeriodo"),

    path('Ri/Curso<int:id_curso>/Asignaturas', views.asignatura, name = "asignatura"),
    path('Ri/Curso<int:id_curso>/Asignaturas/EditarAsignatura<int:id_asignatura>', views.editarAsignatura, name = "editarAsignatura"),
    path('Ri/Curso<int:id_curso>/Asignaturas/EliminarAsignatura<int:id_asignatura>', views.eliminarAsignatura, name = "eliminarAsignatura"),
    path('Ri/Curso<int:id_curso>/Asignatura<int:asgn_id>/Notas', views.alumnosNotas, name = "alumnosNotas"),

]