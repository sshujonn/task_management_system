from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    project_name = models.CharField(max_length=50)
    project_details = models.CharField(max_length=50)
    deadline = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name