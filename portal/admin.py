from django.contrib import admin
from .forms import UserCreationForm
from .models import User, Asignatura, Clase, Curso, Evaluacion, Periodo

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email','fecha_nacimiento','direccion', 'telefono',)
    list_display_links = ('username',)
    list_editable = ('first_name', 'last_name', 'email','fecha_nacimiento','direccion', 'telefono',)


admin.site.register(Asignatura)
admin.site.register(Clase)
admin.site.register(Curso)
admin.site.register(Evaluacion)
admin.site.register(Periodo)
