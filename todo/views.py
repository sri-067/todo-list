from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import TaskForm, CategoryForm, UserRegisterForm
from .models import Task, Category


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after registration
            return redirect('task_list')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})



from datetime import date
from django.shortcuts import render
from .models import Task, Category

@login_required
def task_list(request):
    from datetime import date
    tasks = Task.objects.filter(user=request.user).order_by('position')
    categories = Category.objects.filter(user=request.user)

    # Search and filters (already added previously)
    query = request.GET.get('search')
    if query:
        tasks = tasks.filter(models.Q(title__icontains=query) | models.Q(description__icontains=query))

    if request.GET.get('important') == '1':
        tasks = tasks.filter(important=True)
    if request.GET.get('completed') == '1':
        tasks = tasks.filter(completed=True)
    elif request.GET.get('completed') == '0':
        tasks = tasks.filter(completed=False)

    category_id = request.GET.get('category')
    if category_id:
        tasks = tasks.filter(category_id=category_id)

    sort = request.GET.get('sort')
    if sort == 'due_asc':
        tasks = tasks.order_by('due_date')
    elif sort == 'due_desc':
        tasks = tasks.order_by('-due_date')

    # ✅ Progress stats
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    progress_percent = int((completed_tasks / total_tasks) * 100) if total_tasks else 0

    return render(request, 'task_list.html', {
        'tasks': tasks,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'today': date.today(),
        'progress_percent': progress_percent,
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
    })


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)  # ✅
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)  # ✅
    return render(request, 'edit_task.html', {'form': form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'confirm_delete.html', {'task': task})

from .forms import CategoryForm
from .models import Category

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('task_list')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
        form.fields['category'].queryset = Category.objects.filter(user=request.user)
    return render(request, 'add_task.html', {'form': form})


from django.views.decorators.http import require_POST

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@login_required
def toggle_important(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.important = not task.important
    task.save()
    return JsonResponse({'important': task.important})

@csrf_exempt
@login_required
def toggle_completed(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'status': 'ok', 'completed': task.completed})

@csrf_exempt
@login_required
def reorder_tasks(request):
    data = json.loads(request.body)
    for item in data.get('order', []):
        Task.objects.filter(pk=item['id'], user=request.user).update(position=item['position'])
    return JsonResponse({'status': 'ok'})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm

from .forms import ProfileForm, AdminProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def profile(request):
    # Decide which form to use
    if request.user.is_superuser:
        form_class = AdminProfileForm
    else:
        form_class = ProfileForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = form_class(instance=request.user)

    return render(request, 'profile.html', {'form': form})


from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

from .models import Notification

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})


# example logic (simplified check)
from datetime import date, timedelta
from .models import Task

@login_required
def check_due_tasks(request):
    tomorrow = date.today() + timedelta(days=1)
    tasks = Task.objects.filter(user=request.user, due_date=tomorrow, completed=False)
    for task in tasks:
        Notification.objects.get_or_create(
            user=request.user,
            message=f"Reminder: '{task.title}' is due tomorrow!"
        )
    return JsonResponse({'status': 'ok'})

from django.utils.timezone import now
from django.contrib.auth.models import User
from django.http import JsonResponse

@login_required
def check_due_tasks(request):
    today = now().date()
    due_tasks = Task.objects.filter(user=request.user, due_date=today, completed=False)
    overdue_tasks = Task.objects.filter(user=request.user, due_date__lt=today, completed=False)

    notifications = []

    for task in overdue_tasks:
        notifications.append({
            'message': f"Task '{task.title}' is overdue!",
            'type': 'danger'
        })

    for task in due_tasks:
        notifications.append({
            'message': f"Task '{task.title}' is due today!",
            'type': 'warning'
        })

    return JsonResponse({'notifications': notifications})
@login_required
def notifications_view(request):
    return render(request, 'notifications.html')

