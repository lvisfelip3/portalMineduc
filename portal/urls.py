from django.urls import path
from . import  views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('perfil/', views.perfil, name="perfil"),
    path('perfilAdmin/', views.perfil_ri, name="perfil_ri"),
    path('CrearUsuario/', views.signup, name="signup"),
    path('logout/', views.signout, name='logout'),
    path('IniciarSesion/', views.signin, name='signin'),
    path('Cursos/', views.cursos, name='cursos'),
    path('Cursos/Curso<int:curso_id>', views.editarCursos, name='editarCursos'),
    path('Cursos/Curso<int:curso_id>/delete', views.eliminarCursos, name='eliminarCursos'),
    path('Cursos/Lista/Curso<int:curso_idd>', views.estudiantesCursos, name="listaEst"),
    path('Cursos/delete/Curso<int:curso_idd>/Usuario<int:usuario_id>', views.eliminarAlumnoCurso, name="eliminarAlumnoCurso"),
    path('Periodo', views.periodo, name = "periodo"),
]