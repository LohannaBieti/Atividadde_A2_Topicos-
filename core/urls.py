from django.urls import path
from . import views
from .views import register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('tarefa/nova/', views.task_create, name='task_create'),
    path('tarefa/editar/<int:pk>/', views.task_edit, name='task_edit'),
    path('tarefa/excluir/<int:pk>/', views.task_delete, name='task_delete'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
]