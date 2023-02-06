# from django.forms import ModelForm
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['titulo', 'descripcion']
    widgets = {
      'titulo': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Escriba un título para la tarea'}),
      'descripcion': forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'Escriba una descripción para la tarea'})
    }
