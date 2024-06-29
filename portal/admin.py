from django.contrib import admin
from .models import User, Asignatura, Clase, Curso, Evaluacion, Periodo


admin.site.register(User)
admin.site.register(Asignatura)
admin.site.register(Clase)
admin.site.register(Curso)
admin.site.register(Evaluacion)
admin.site.register(Periodo)