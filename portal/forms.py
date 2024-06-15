from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Curso, User, Periodo
from django.contrib.auth.models import Group

class crearCurso(forms.ModelForm):
    nombre = forms.CharField(label='Curso', required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder':'Nombre'}))

    class Meta:
        model = Curso
        fields = '__all__'


class CustomUserCreation(UserCreationForm):
    Usuario = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.Select)
    class Meta:
        model = User
        fields = ('username','curso','first_name','last_name','telefono',)

class crearPeriodo(forms.ModelForm):
    fecha_fin = forms.CharField(label='Fecha fin',required=True, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder':'Ingresa una Fecha','type':'date'}))
    fecha_inicio = forms.CharField(label='Fecha inicio',required=True, widget=forms.DateInput(format=('%Y-%m-%d'), attrs={'placeholder':'Ingresa una Fecha','type':'date'}))
    predeterminado = forms.BooleanField(label='Predeterminado', required=False)
    class Meta:
        model = Periodo
        fields = ('nombre','fecha_inicio','fecha_fin',)