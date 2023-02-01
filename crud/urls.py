from django.urls import path
from . import views
from .views import cerrar_sesion, signin, create_tasks, task_detail, completed_task

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/create/', views.create_tasks, name="create_tasks"),
    path('tasks/<int:task_id>/', views.task_detail, name="task_detail"),
    path('tasks/<int:task_id>/complete/', views.completed_task, name="completed_task"),
    path('logout/', views.cerrar_sesion, name="logout"),
    path('signin/', views.signin, name="signin")
    # path('delete_task/', views.delete_task, name="delete_task")
    
]