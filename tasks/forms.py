from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, \
    SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User

from tasks.models import Task
from django import forms

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'reminder_time']


class DisplayTaskForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    reminder_time = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control'}))

    # reminder_time = forms.DateTimeField(
    #     input_formats=['%d/%m/%y %I:%M %p'],
    #     widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input','data-target': '#datetimepicker1'
    #     })
    # )