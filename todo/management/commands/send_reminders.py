from django.core.management.base import BaseCommand
from django.utils import timezone
from todo.models import Task
from django.contrib.auth.models import User
from django.contrib import messages

class Command(BaseCommand):
    help = 'Send reminders for tasks due today'

    def handle(self, *args, **kwargs):
        today = timezone.localdate()
        due_tasks = Task.objects.filter(due_date=today, completed=False)

        if due_tasks.exists():
            self.stdout.write(f"Found {due_tasks.count()} task(s) due today.")
            for task in due_tasks:
                self.stdout.write(f"- {task.title} (User: {task.user.username})")
                # If you want to send a real notification/email, do it here.
        else:
            self.stdout.write("No tasks due today.")
