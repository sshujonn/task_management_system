from django.http import HttpResponseRedirect
from django.core import serializers as c_serializers

# Create your views here.
from django.urls import reverse
from django.contrib import messages
from rest_framework import renderers, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from helper.PermissionUtil import DBCRUDPermission
from helper.global_service import GlobalService
from projects.models import Project

gs = GlobalService()
class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'project_name',
            'project_details',
            'deadline',
        )

class ProjectFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'




class ProjectCreate(APIView):
    permission_classes = (IsAuthenticated,DBCRUDPermission)
    template_name = 'dashboard/project/create_project_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        serializer = ProjectSerializer()
        return Response({'serializer': serializer, 'menu': menu},template_name=self.template_name)


    def post(self, request):
        modified_data = gs.update_immutable_obj(request.data,{'created_by':request.user.id, 'last_updated_by': request.user.pk})
        serializer = ProjectFieldsSerializer(context=request,data=modified_data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse('view_project'))



class ProjectList(APIView):
    permission_classes = (IsAuthenticated, DBCRUDPermission)
    template_name = 'dashboard/project/view_projects.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        projects = Project.objects.filter(created_by=request.user.id)
        projects = c_serializers.serialize("python", projects)
        return Response({'serializer': projects, 'menu': menu}, template_name=self.template_name)


class ProjectsEdit(APIView):
    permission_classes = (IsAuthenticated,)
    template_name = 'dashboard/project/edit_project_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request, pk, action=None):
        project = Project.objects.filter(created_by=request.user.id)

        if (len(project)<1):
            messages.warning(request, 'Only creator of this project can update')
            return HttpResponseRedirect(reverse('view_project'))
        project = project.get(pk=pk)
        if action == 'delete':
            project.delete()
        else:
            serializer = ProjectSerializer(project)
            return Response({'serializer': serializer, 'project': project},template_name=self.template_name)

        return HttpResponseRedirect(reverse('view_project'))

    def post(self, request, pk, action):
        project = Project.objects.filter(created_by=request.user.id).get(pk=pk)
        serializer = ProjectSerializer(project, data=request.data)

        if action=='update':
            if serializer.is_valid():
                serializer.save()

        return HttpResponseRedirect(reverse('view_project'))