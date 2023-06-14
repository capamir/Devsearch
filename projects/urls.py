from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectsView.as_view(), name='projects'),

    path('create-project/', views.CreateProjectView.as_view(), name="create-project"),

    path('project/<str:pk>/', views.ProjectDetailsView.as_view(), name="project"),

    path('update-project/<str:pk>/',
         views.UpdateProjectView.as_view(), name="update-project"),

    path('delete-project/<str:pk>/',
         views.DeleteProjectView.as_view(), name="delete-project"),
]
