"""task_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from tasks import views as task_views
from projects import views as project_views
from profiles import views


urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),

    path('sign-up/', views.sign_up, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('sign-in/', views.sign_in, name='signin'),
    path('sign-out/', views.sign_out, name='logout'),
    path('task-entry/', task_views.task_entry, name='task_entry'),
    path('task-history/', task_views.task_history, name='task_history'),


    # path('task-update/', task_views.task_history, name='task_history'),

    path('', views.dashboard, name="dashboard"),

    path('task-edit/<int:pk>/<slug:action>', task_views.TasksEdit.as_view(),
         name="task_edit"),

    path('create_project/', project_views.ProjectCreate.as_view(), name='create_project'),
    path('view_project/', project_views.ProjectList.as_view(), name='view_project'),
    path('edit-project/<int:pk>/<slug:action>', project_views.ProjectsEdit.as_view(),
             name="update_project"),
]

admin.site.site_header = "Task Manager"
admin.site.index_title = "Task Manager"
admin.site.site_title = "Task Manager"
