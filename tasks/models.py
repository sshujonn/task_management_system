from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from profiles.models import Profile
# Create your models here.
class Task(models.Model):
    name = models.TextField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    reminder_time = models.DateTimeField()
    assigned_at = models.DateTimeField()
    deadline = models.DateTimeField()
    progress = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
     )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    #TODO:: Add more needed field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
