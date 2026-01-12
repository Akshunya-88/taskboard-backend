from django.db import models
from django.utils.translation import gettext_lazy as _

class TaskStatus(models.TextChoices):
    TODO = 'todo', _('To Do')
    IN_PROGRESS = 'in-progress', _('In Progress')
    DONE = 'done', _('Done')

class TaskPriority(models.TextChoices):
    LOW = 'low', _('Low')
    MEDIUM = 'medium', _('Medium')
    HIGH = 'high', _('High')