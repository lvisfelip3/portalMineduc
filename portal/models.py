from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from django.db import transaction

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
    edad = models.CharField(max_length=3, default='')
    direccion = models.CharField(max_length=50, default='')
    telefono = models.CharField(max_length=10, default='')
    imagenPerfil = models.ImageField(upload_to="imagen_perfil", null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, default='')
    groups = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, default='')


    def __str__(self):
        return self.username
    

class Dia(models.Model):
    nombre = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre
    


class Asignatura(models.Model):
    nombre = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre
    
class Clase(models.Model):
    nombre = models.CharField(max_length=30)
    hora_inicio = models.TimeField(blank=False)
    hora_termino = models.TimeField(blank=False)
    asistencia = models.BooleanField(default=False)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class Evaluacion(models.Model):
    nombre = models.CharField(max_length=20)
    nota1 = models.IntegerField(null=True, blank=True)
    nota2 = models.IntegerField(null=True, blank=True)
    nota3 = models.IntegerField(null=True, blank=True)
    promedio = models.IntegerField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

