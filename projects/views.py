from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from .models import Project, Tag
from .forms import ReviewForm, ProjectForm

# Create your views here.


class ProjectsView(View):
    template_name = 'projects/projects.html'

    def get(self, request, *args, **kwargs):
        self.projects = self._search_projects(request)
        custom_range = self._paginate(request, 3)

        context = {
            'projects': self.projects,
            'search_query': self.search_query,
            'custom_range': custom_range
        }
        return render(request, self.template_name, context)

    def _search_projects(self, request):
        query = request.GET.get('search_query')
        self.search_query = query if query else ''

        tags = Tag.objects.filter(name__icontains=self.search_query)

        projects = Project.objects.distinct().filter(
            Q(title__icontains=self.search_query) |
            Q(description__icontains=self.search_query) |
            Q(owner__name__icontains=self.search_query) |
            Q(tags__in=tags)
        )

        return projects

    def _paginate(self, request, results):
        page = request.GET.get('page')
        paginator = Paginator(self.projects, results)

        try:
            self.projects = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            self.projects = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            self.projects = paginator.page(page)

        first_page = (int(page) - 4)
        leftIndex = first_page if first_page >= 1 else 1

        last_page = (int(page) + 5)
        num_pages = paginator.num_pages
        rightIndex = last_page if last_page > num_pages else num_pages + 1

        custom_range = range(leftIndex, rightIndex)

        return custom_range


class ProjectDetailsView(View):
    template_name = 'projects/details.html'
    form_class = ReviewForm

    def setup(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, id=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'project': self.project,
            'form': self.form_class
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = self.project
            review.owner = request.user.profile
            review.save()

            self.project.getVoteCount
            messages.success(
                request, 'Your review was successfully submitted!')
            return redirect('projects:project', pk=self.project.id)

        context = {
            'project': self.project,
            'form': form
        }
        return render(request, self.template_name, context)


class CreateProjectView(LoginRequiredMixin, View):
    template_name = 'projects/create.html'
    form_class = ProjectForm

    def setup(self, request, *args, **kwargs):
        self.profile = request.user.profile
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwards):
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = self.profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('accounts:account')

        context = {'form': self.form_class}
        return render(request, self.template_name, context)


class UpdateProjectView(LoginRequiredMixin, View):
    template_name = 'projects/update.html'
    form_class = ProjectForm

    def setup(self, request, *args, **kwargs):
        self.profile = request.user.profile
        self.project = self.profile.project_set.get(id=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not self.project.owner.id == self.profile.id:
            messages.error(request, 'you cant update this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.project)

        context = {'form': form, 'project': self.project}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = self.form_class(
            request.POST, request.FILES, instance=self.project)
        if form.is_valid():
            project = form.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('accounts:account')

        context = {'form': form}
        return render(request, self.template_name, context)


class DeleteProjectView(LoginRequiredMixin, View):
    template_name = 'delete.html'

    def setup(self, request, *args, **kwargs):
        self.profile = request.user.profile
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.project = self.profile.project_set.get(id=kwargs['pk'])
        context = {'object': self.project}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        self.project.delete()
        return redirect('projects:projects')
