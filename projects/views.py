from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from rest_framework import renderers, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'




class ProjectCreate(APIView):
    permission_classes = (IsAuthenticated,)
    template_name = 'dashboard/project/create_project_page.html'
    renderer_classes = [renderers.TemplateHTMLRenderer]

    def get(self, request):
        menu = gs.get_menu(request.user)
        serializer = ProjectSerializer()
        return Response({'serializer': serializer, 'menu': menu},template_name=self.template_name)


    def post(self, request):
        modified_data = gs.update_immutable_obj(request.data,{'created_by':request.user.id, 'last_updated_by': request.user.pk})
        serializer = ProjectCreateSerializer(context=request,data=modified_data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponseRedirect(reverse('task_entry'))