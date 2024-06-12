from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Curso, User

class crearCurso(forms.ModelForm):
    nombre = forms.CharField(label='Curso', required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder':'Nombre'}))

    class Meta:
        model = Curso
        fields = '__all__'


class CustomUserCreation(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','curso',)