from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import serializers, renderers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
# Create your views here.
from helper.PermissionUtil import DBCRUDPermission
from profiles.models import Profile
from tasks.forms import TaskForm, DisplayTaskForm

from tasks.models import Task

from rest_framework import generics
from django.core import serializers as c_serializers
from helper.global_service import GlobalService
from tasks.serializers import TaskSerializer
from datetime import datetime

gs = GlobalService()

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
            'assigned_at',
            'deadline',
            'progress',
            'assigned_to',
            'project',
        )

class TaskAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('__all__')

class TaskCreate(APIView):
    permission_classes = (IsAuthenticated,DBCRUDPermission)
    template_name = 'dashboard/task/create_task_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        serializer = TaskSerializer()
        return Response({'serializer': serializer, 'menu': menu},template_name=self.template_name)


    def post(self, request):
        # import pdb;pdb.set_trace()
        modified_data = gs.update_immutable_obj(request.data,{'created_by':request.user.id, 'assigned_by': request.user.pk})
        serializer = TaskAllSerializer(context=request,data=modified_data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse('view_task'))

# class LargeResultsSetPagination(PageNumberPagination):
#     page_size = 1
#     page_size_query_param = 'page_size'
#     max_page_size = 1

class TaskList(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/task/view_tasks.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]
    # pagination_class = LargeResultsSetPagination

    def get(self, request):
        menu = gs.get_menu(request.user)
        tasks = Task.objects.filter()
        tasks = c_serializers.serialize("python", tasks)
        return Response({'serializer': tasks, 'menu': menu}, template_name=self.template_name)

class TasksEdit(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/task/edit_task_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request, pk, action=None):
        menu = gs.get_menu(request.user)
        task = Task.objects.filter(Q(created_by=request.user.pk) | Q(assigned_by=request.user.pk)| Q(assigned_to=request.user)).get(pk=pk)

        if action == 'delete':
            task.delete()
        else:
            serializer = TaskSerializer(task)
            return Response({'serializer': serializer, 'menu': menu, 'task': task},template_name=self.template_name)

        return HttpResponseRedirect(reverse('view_task'))

    def post(self, request, pk, action):
        task = Task.objects.filter(Q(created_by=request.user.pk) | Q(assigned_by=request.user.pk)).get(pk=pk)
        serializer = TaskSerializer(task, data=request.data)

        if action=='update':
            if serializer.is_valid():
                serializer.save()

        return HttpResponseRedirect(reverse('view_task'))

