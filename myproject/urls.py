from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from todo import views

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),  # ✅ This enables /admin/

    # Your To-Do app views
    path('profile/', views.profile, name='profile'),
    path('profile/', views.profile_view, name='profile'),
    path('toggle-completed/<int:pk>/', views.toggle_completed, name='toggle_completed'),
    path('register/', views.register, name='register'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', views.task_list, name='task_list'),
    path('reorder-tasks/', views.reorder_tasks, name='reorder_tasks'),
    path('add/', views.add_task, name='add_task'),
    path('toggle-important/<int:pk>/', views.toggle_important, name='toggle_important'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html')),
]
from django.contrib.auth import views as auth_views

urlpatterns += [
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='password_change_done'),
]
urlpatterns += [
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]

from django.urls import path
from todo import views

urlpatterns += [
    path('notifications/', views.notifications_view, name='notifications'),
    path('check-due-tasks/', views.check_due_tasks, name='check_due_tasks'),
]

