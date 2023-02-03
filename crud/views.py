from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import *
# from django.utils import timezone
from datetime import date
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
  return render(request, 'home.html')

@login_required
def tasks(request):
  lista = Task.objects.filter(user=request.user, completada__isnull=True)
  return render(request, 'tasks.html', {'objetos':lista})

@login_required
def tasks_completed(request):
  lista = Task.objects.filter(user=request.user, completada__isnull=False).order_by('-completada')
  # fecha = datetime.datetime.now() #sirve para tener fecha y hora en tiempo real, realizando previamente import datetime
  fecha = date.today()
  return render(request, 'tasks_completed.html', {'completadas':lista, 'date':fecha })

@login_required
def create_tasks(request):
  if request.method == 'GET':
    return render(request, 'create_task.html', { 'form': TaskForm })
  else:
    if request.POST['descripcion'] == '':
      crear = render(request, 'create_task.html', { 'form': TaskForm, 'error': 'la descripcion debe llenarse' })
      return crear
    else:
      form = TaskForm(request.POST)
      task_new = form.save(commit=False)
      task_new.user = request.user
      task_new.save()
      return redirect('tasks')

def signup(request):
  if request.method == 'GET':
    return render(request, 'signup.html', {'form': UserCreationForm})
  else:
    if request.POST['password1'] == request.POST['password2']:
      try:
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
        user.save()
        login(request, user)
        return redirect('tasks')
      # MANEJO DE ERRORES
      except IntegrityError:
        return render(request, 'signup.html', {'form': UserCreationForm, 'error': "El ususario ya existe"})

    return render(request, 'signup.html', {'form': UserCreationForm, 'error': "Las contraseñas no coinciden"})

def cerrar_sesion(request):
  logout(request)
  return redirect('home')  # redirect tiene como parametro la URL

def signin(request):
  if request.method == 'GET':
    return render(request, 'signin.html', {
      'form': AuthenticationForm
    })
  else:
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
      return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Credenciales no validas'})
    else:
      login(request, user)
      return redirect('tasks')

# OBTENER y ACTUALIZAR TAREA
@login_required
def task_detail(request, task_id):
  if request.method == 'GET':
    # task = Task.objects.get(pk=task_id)
    task = get_object_or_404(Task, pk=task_id, user=request.user) #se pasa el modelo a consultar (Task) y se obtiene la tarea
    form = TaskForm(instance = task)
    return render(request, 'task_detail.html', { 'task': task, 'form': form })
  else:
      if request.POST['descripcion'] == '':
        task = get_object_or_404(Task, pk=task_id, user=request.user) #obtener nuevamente la tarea porque 'else' ya es otro bloque
        form = TaskForm(request.POST, instance = task)
        return render(request, 'task_detail.html', { 'task': task, 'form': form, 'error': 'La descripcion no debe estar vacía' })
      else:
        try:
          task = get_object_or_404(Task, pk=task_id, user=request.user) #obtener nuevamente la tarea porque 'else' ya es otro bloque
          form = TaskForm(request.POST, instance = task)#obtiene todos los datos : request.POST
          form.save()
          return redirect('tasks')
        except ErrorValue:
          return render(request, 'task_detail.html', { 'task': task, 'form': form, 'error': 'Error al actualizar' })

# TAREA COMPLETADA : ELIMINADA
@login_required
def completed_task(request, task_id):
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  try:
    if request.method == 'POST':
      form = TaskForm(request.POST, instance = task)#obtiene todos los datos : request.POST
      form.save()
  except:
    # if request.method == 'POST':
    # task.completada = timezone.now()    
    task.save()
  return redirect('tasks')

# @login_required
# def delete_task(request, task_id):
#   task = get_object_or_404(Task, pk=task_id, user=request.user)
#   if request.method == 'POST':
#     task.delete()
#     return redirect('tasks')

@login_required
def delete_task_completed(request, task_id):
  task = get_object_or_404(Task, pk=task_id, user=request.user)
  if request.method == 'POST':
    task.delete()
    return redirect('tasks_completed')




















