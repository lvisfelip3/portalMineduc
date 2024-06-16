from django.urls import path
from . import  views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('perfil/', views.perfil, name="perfil"),
    path('perfilAdmin/', views.perfil_ri, name="perfil_ri"),
    path('perfilAdmin/CrearUsuario/', views.signup, name="signup"),
    path('logout/', views.signout, name='logout'),
    path('IniciarSesion/', views.signin, name='signin'),
    path('perfilAdmin/Periodo<int:id_periodo>/Cursos/', views.cursos, name='cursos'),
    path('perfilAdmin/Cursos/Curso<int:curso_id>/Periodo<int:id_periodo>', views.editarCursos, name='editarCursos'),
    path('perfilAdmin/Cursos/Curso<int:curso_id>/Periodo<int:id_periodo>/delete', views.eliminarCursos, name='eliminarCursos'),
    path('perfilAdmin/Cursos/Lista/Curso<int:curso_idd>', views.estudiantesCursos, name="listaEst"),
    path('perfilAdmin/Cursos/delete/Curso<int:curso_idd>/Usuario<int:usuario_id>', views.eliminarAlumnoCurso, name="eliminarAlumnoCurso"),
    path('perfilAdmin/Periodo', views.periodo, name = "periodo"),
    path('perfilAdmin/editarPeriodo/Periodo<int:periodo_id>', views.editarPeriodo, name = "editarPeriodo"),
    path('perfilAdmin/editarPeriodo/Periodo<int:periodo_id>/delete', views.eliminarPeriodo, name = "eliminarPeriodo"),
]