from django.shortcuts import render, redirect
from django.views.generic import (
    FormView, CreateView,
    ListView, DetailView,
    View)
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserLoginForm, UserCreationForm
from .models import Profile
# Create your views here.


class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'accounts/auth/login.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:profiles')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self._login_user(form.cleaned_data)
        return super().form_valid(form)

    def _login_user(self, data):
        user = authenticate(
            self.request,
            username=data['username'],
            password=data['password']
        )
        if user:
            login(self.request, user)
            messages.success(
                self.request, 'You logged in successfully', 'info')
        else:
            self.form_invalid(data)
            messages.error(
                self.request, 'username or password is incorrect', 'warning')

        return user


class LogoutView(LoginRequiredMixin, LogoutView):
    next_page = '/'


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/auth/register.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:profiles')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request, 'you registered successfully', 'success')
        return super().form_valid(form)


class ProfilesView(ListView):
    template_name = 'accounts/profiles.html'
    model = Profile
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    template_name = 'accounts/profile_detail.html'
    model = Profile
    context_object_name = 'profiles'

    def get(self, request, **kwargs):
        self.object = self.get_object()

        context = self.get_context_data(object=self.object)

        topSkills = self.object.skill_set.exclude(description__exact="")
        context['topSkills'] = topSkills

        otherSkills = self.object.skill_set.filter(description="")
        context['otherSkills'] = otherSkills

        return self.render_to_response(context)


class UserProfileView(View):
    template_name = 'accounts/account.html'

    def setup(self, request, *args, **kwargs):
        self.profile = request.user.profile
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        skills = self.profile.skill_set.all()
        projects = self.profile.project_set.all()
        context = {
            'profile': self.profile,
            'projects': projects,
            'skills': skills
        }
        return render(request, self.template_name, context)
