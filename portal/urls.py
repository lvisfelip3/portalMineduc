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
    #--------------------------------------------------
    #--------------- ADMIN Y DOCENTE-------------------
    #--------------------------------------------------
    path('<int:id_user>/', views.perfil_ri, name="perfil_ri"),

    path('<int:id_user>/CrearUsuario/Estudiante', views.signupEstudiante, name="signupEstudiante"),
    path('<int:id_user>/CrearUsuario/Docente', views.signupDocente, name="signupDocente"),
    path('<int:id_user>/CrearUsuario/RI', views.signupRI, name="signupRI"),

    path('<int:id_user>/Periodo<int:id_periodo>/Curso<int:id_curso>/Asistencia', views.asistenciasCurso, name='asistenciasCurso'),
    path('<int:id_user>/Curso<str:fecha_asistencia>/Asistencia/delete', views.eliminarAsistencia, name='eliminarAsistencia'),
    path('<int:id_user>/Periodo<int:id_periodo>/CursosAsistencia/', views.listaCurso, name='listaCursos'),
    path('<int:id_user>/Periodo<int:id_periodo>/Curso<int:id_curso>/RegistroAsistencia', views.registrarAsistencia, name = "asistencia"),
    path('<int:id_user>/Curso<int:id_curso>/<str:fecha_asistencia>/RegistroAsistencia', views.listaAsistencia, name = "listaAsistencia"),


    path('<int:id_user>/Periodo<int:id_periodo>/Curso<int:id_curso>/Clases', views.horarioPorCurso, name = "horarioCurso"),

    
    path('<int:id_user>/Periodo<int:id_periodo>/Cursos/', views.cursos, name='cursos'),
    path('<int:id_user>/Cursos/Curso<int:curso_id>/Periodo<int:id_periodo>', views.editarCursos, name='editarCursos'),
    path('<int:id_user>/Cursos/Curso<int:curso_id>/Periodo<int:id_periodo>/delete', views.eliminarCursos, name='eliminarCursos'),

    path('<int:id_user>/Cursos/Lista/Curso<int:curso_idd>', views.estudiantesCursos, name="listaEst"),
    path('<int:id_user>/Cursos/delete/Curso<int:curso_idd>/Usuario<int:usuario_id>', views.eliminarAlumnoCurso, name="eliminarAlumnoCurso"),

    path('<int:id_user>/Periodo', views.periodo, name = "periodo"),
    path('<int:id_user>/editarPeriodo/Periodo<int:periodo_id>', views.editarPeriodo, name = "editarPeriodo"),
    path('<int:id_user>/editarPeriodo/Periodo<int:periodo_id>/delete', views.eliminarPeriodo, name = "eliminarPeriodo"),

    path('<int:id_user>/Curso<int:id_curso>/Asignaturas', views.asignatura, name = "asignatura"),
    path('<int:id_user>/Curso<int:id_curso>/Asignaturas/EditarAsignatura<int:id_asignatura>', views.editarAsignatura, name = "editarAsignatura"),
    path('<int:id_user>/Curso<int:id_curso>/Asignaturas/EliminarAsignatura<int:id_asignatura>', views.eliminarAsignatura, name = "eliminarAsignatura"),
    path('<int:id_user>/Curso<int:id_curso>/Asignatura<int:asgn_id>/Notas', views.alumnosNotas, name = "alumnosNotas"),

]