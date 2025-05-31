from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default='secondary')  # Accepts Bootstrap color class names
    icon = models.CharField(max_length=50, blank=True)  # Optional icon class (e.g. bi bi-star)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    due_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    position = models.PositiveIntegerField(default=0)  # ✅ Add this line

    class Meta:
        ordering = ['position']  # ✅ Ensures default order

    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User
from django.db import models

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Read' if self.is_read else 'Unread'}"

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)  # ✅ Add null=True
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    position = models.PositiveIntegerField(default=0)
    reminder_sent = models.BooleanField(default=False)  # ✅ New field

