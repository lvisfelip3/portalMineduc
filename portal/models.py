from django.db import models, transaction
from django.contrib.auth.models import AbstractUser,Group

class Periodo(models.Model):
    nombre = models.CharField(max_length=20)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    predeterminado = models.BooleanField(default=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.predeterminado:
            return super(Periodo, self).save(*args, **kwargs)
        with transaction.atomic():
            Periodo.objects.filter(
                predeterminado=True).update(predeterminado=False)
            return super(Periodo, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

seccion = [
    ['A', 'A'],
    ['B', 'B']
]

class Curso(models.Model):
    nombre = models.CharField(max_length=20)
    seccion = models.CharField(choices= seccion, default='A', max_length=2)
    periodo = models.ForeignKey(Periodo, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class User(AbstractUser):
    edad = models.IntegerField(null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True)
    direccion = models.CharField(max_length=50, null=True)
    telefono = models.CharField(max_length=10, null=True)
    imagenPerfil = models.ImageField(upload_to="imagen_perfil", null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True)
    groups = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username
    
class Asignatura(models.Model):
    nombre = models.CharField(max_length=40)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.nombre
    

class Clase(models.Model):
    nombre = models.CharField(max_length=30, null=True)
    hora = models.CharField(max_length=6)
    dia = models.CharField(max_length=10)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class Evaluacion(models.Model):
    nota1 = models.IntegerField(null=True, blank=True)
    nota2 = models.IntegerField(null=True, blank=True)
    nota3 = models.IntegerField(null=True, blank=True)
    nota4 = models.IntegerField(null=True, blank=True)
    nota5 = models.IntegerField(null=True, blank=True)
    nota6 = models.IntegerField(null=True, blank=True)
    nota7 = models.IntegerField(null=True, blank=True)
    nota8 = models.IntegerField(null=True, blank=True)
    nota9 = models.IntegerField(null=True, blank=True)
    promedio = models.IntegerField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Asistencia(models.Model):
    fecha = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    asistio = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.nombre} - {self.fecha}"