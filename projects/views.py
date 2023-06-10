from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class ProjectsView(TemplateView):
    template_name = 'projects/home.html'
    