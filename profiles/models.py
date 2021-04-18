from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Profile(User):

    class SalutationChoices(models.TextChoices):
        MISTER = 'Mr.', _('Mister')
        MISTRESS = 'Ms.', _('Mistress')

    class DesignationChoices(models.TextChoices):
        ASSISTANT_OFFICER = 'AO', _('Assistant Officer')
        OFFICER = 'O', _('Officer')
        MT_OFFICER = 'MTO', _('Management Trainee Officer')
        SENIOR_OFFICER = 'SO', _('Senior Officer')

    is_email_verified =  models.BooleanField(default=False)
    is_authorized = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    salutation = models.CharField(max_length=3, choices=SalutationChoices.choices, default=SalutationChoices.MISTER)
    designation = models.CharField(max_length=3, choices=DesignationChoices.choices, default='')
