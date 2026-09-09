from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TaskForm
from .models import Task
from django.contrib.auth import login


def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('dashboard')
  else:
    form = UserCreationForm()
    for field in form.fields.values():
        field.help_text = None
  return render(request, 'core/register.html', {'form': form})


@login_required
def dashboard(request):
  tasks = Task.objects.filter(user=request.user)

  status_filter = request.GET.get('status')
  if status_filter:
    tasks = tasks.filter(status=status_filter)

  context = {'tasks': tasks, 'current_status': status_filter}
  return render(request, 'core/dashboard.html', context)


@login_required
def task_create(request):
  if request.method == 'POST':
    form = TaskForm(request.POST)
    if form.is_valid():
      task = form.save(commit=False)
      task.user = request.user
      task.save()
      return redirect('dashboard')
  else:
    form = TaskForm()
  return render(request, 'core/task_form.html', {'form': form})


@login_required
def task_edit(request, pk):
  task = get_object_or_404(Task, pk=pk, user=request.user)
  if request.method == 'POST':
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
      form.save()
      return redirect('dashboard')
  else:
    form = TaskForm(instance=task)
  return render(request, 'core/task_form.html', {'form': form})


@login_required
def task_delete(request, pk):
  task = get_object_or_404(Task, pk=pk, user=request.user)
  if request.method == 'POST':
    task.delete()
    return redirect('dashboard')
  return render(request, 'core/task_confirm_delete.html', {'task': task})