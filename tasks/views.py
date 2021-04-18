from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import serializers, renderers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
# Create your views here.
from profiles.models import Profile
from tasks.forms import TaskForm, DisplayTaskForm

from tasks.models import Task

from rest_framework import generics

from tasks.serializers import TaskSerializer
from datetime import datetime


def task_entry(request):
    if request.user.is_authenticated:
        form = DisplayTaskForm(request.POST)
        if form.is_valid():
            name = form.data.get('name')
            description = form.data.get('description')
            reminder_time = form.data.get('reminder_time')
            reminder_time = datetime.strptime(reminder_time, "%d/%m/%Y %H:%M")
            task = Task(
                name=name,
                description=description,
                reminder_time=reminder_time,
                user=User.objects.get(pk=request.user.id)
            )
            task.save()
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return HttpResponseRedirect(reverse('signin'))


def task_history(request):
    if request.user.is_authenticated:

        tasks = Task.objects.filter(user=request.user).filter(reminder_time__lt=datetime.now())

        return render(request, 'task_history.html', {'tasks': tasks})
    else:
        return HttpResponseRedirect(reverse('signin'))


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'description',
            'reminder_time',
        )

class TasksEdit(APIView):
    permission_classes = (IsAuthenticated,)
    template_name = 'edit_task_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, pk, action=None):
        task = Task.objects.filter(user=request.user).get(pk=pk)

        if action == 'delete':
            task.delete()
        else:
            serializer = TaskSerializer(task)
            return Response({'serializer': serializer, 'task': task},template_name=self.template_name)

        if reverse('task_history') in request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(reverse('task_history'))
        return HttpResponseRedirect(reverse('task_entry'))

    def post(self, request, pk, action):
        task = Task.objects.filter(user=request.user).get(pk=pk)
        serializer = TaskSerializer(task, data=request.data)

        if action=='update':
            if serializer.is_valid():
                serializer.save()
        if reverse('task_history') in request.META.get('HTTP_REFERER'):
            return HttpResponseRedirect(reverse('task_history'))

        return HttpResponseRedirect(reverse('task_entry'))

