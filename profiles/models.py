from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Profile(models.Model):

    class SalutationChoices(models.TextChoices):
        MISTER = 'Mr.', _('Mister')
        MISTRESS = 'Ms.', _('Mistress')

    class DesignationChoices(models.TextChoices):
        ASSISTANT_OFFICER = 'AO', _('Assistant Officer')
        OFFICER = 'O', _('Officer')
        MT_OFFICER = 'MTO', _('Management Trainee Officer')
        SENIOR_OFFICER = 'SO', _('Senior Officer')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    salutation = models.CharField(max_length=3, choices=SalutationChoices.choices, default=SalutationChoices.MISTER)
    designation = models.CharField(max_length=3, choices=DesignationChoices.choices, default='')
