from django.db import models
from django.contrib.auth.models import User
import uuid
from utils.enums import TaskStatus, TaskPriority  # Import your new enums

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=20, default="#000000")

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Using Enums here
    status = models.CharField(
        max_length=20, 
        choices=TaskStatus.choices, 
        default=TaskStatus.TODO
    )
    priority = models.CharField(
        max_length=20, 
        choices=TaskPriority.choices, 
        default=TaskPriority.MEDIUM
    )

    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title