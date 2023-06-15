from typing import Any, Dict
from django import http
from django.shortcuts import render, redirect
from django.views.generic import (
    FormView, CreateView,
    ListView, DetailView,
    View)
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import UserLoginForm, UserCreationForm, ProfileForm, SkillForm, MessageForm
from .models import Profile, Skill
# Create your views here.


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/auth/login.html'
    # success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:profiles')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd.get('username'),
                password=cd.get('password'),
            )
            if user is not None:
                login(request, user)
                messages.success(
                    request, 'You logged in successfully', 'info')
                return redirect('accounts:profiles')
            else:
                messages.error(
                    request, 'username or password is incorrect', 'warning')
                return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        user = self._login_user(form.cleaned_data)
        if user is None:
            return self.form_invalid(form)

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


class ProfilesView(View):
    template_name = 'accounts/profile/profiles.html'

    def get(self, request, *args, **kwargs):
        self.profiles = self._search_profiles(request)
        custom_range = self._paginate(request, 3)

        context = {
            'profiles': self.profiles,
            'search_query': self.search_query,
            'custom_range': custom_range
        }
        return render(request, self.template_name, context)

    def _search_profiles(self, request):
        query = request.GET.get('search_query')
        self.search_query = query if query else ''

        skills = Skill.objects.filter(name__icontains=self.search_query)

        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=self.search_query) |
            Q(short_intro__icontains=self.search_query) |
            Q(skill__in=skills)
        )

        return profiles

    def _paginate(self, request, results):
        page = request.GET.get('page')
        paginator = Paginator(self.profiles, results)

        try:
            self.profiles = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            self.profiles = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            self.profiles = paginator.page(page)

            first_page = (int(page) - 4)
            leftIndex = first_page if first_page >= 1 else 1

            last_page = (int(page) + 5)
            num_pages = paginator.num_pages
            rightIndex = last_page if last_page > num_pages else num_pages + 1

            custom_range = range(leftIndex, rightIndex)

            return custom_range


class ProfileDetailView(DetailView):
    template_name = 'accounts/profile/profile_detail.html'
    model = Profile
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.object = self.get_object()

        topSkills = self.object.skill_set.exclude(description__exact="")
        context['topSkills'] = topSkills

        otherSkills = self.object.skill_set.filter(description="")
        context['otherSkills'] = otherSkills


class UserProfileView(View):
    template_name = 'accounts/profile/account.html'

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


class UpdateUserProfileView(View):
    template_name = 'accounts/profile/profile_form.html'
    form_class = ProfileForm

    def setup(self, request, *args, **kwargs):
        self.profile = request.user.profile
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.profile)
        context = {'form': self.form_class}
        return render(request, self.template, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:account')
        context = {'form': self.form_class}
        return render(request, self.template, context=context)


class CreateSkillView(View):
    template_name = 'accounts/skill/create.html'
    form_class = SkillForm

    def setup(self, request, *args, **kwargs):
        self.profile = request.user.profile
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': self.form_class}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = self.profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('accounts:account')

        context = {'form': form}
        return render(request, self.template_name, context=context)


class UpdateSkillView(View):
    template_name = 'accounts/skill/update.html'
    form_class = SkillForm

    def setup(self, request, *args, **kwargs):
        self.profile = request.user.profile
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        skill = self.profile.skill_set(id=kwargs['pk'])
        form = self.form_class(instance=skill)
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('accounts:account')

        context = {'form': form}
        return render(request, self.template_name, context=context)


class DeleteSkillView(View):
    template_name = 'delete.html'

    def setup(self, request, *args, **kwargs):
        self.profile = request.user.profile
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.skill = self.profile.skill_set(id=kwargs['pk'])
        context = {'object': self.skill}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        self.skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('accounts:account')


class InboxView(View):
    template_name = 'message/inbox.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        message_requests = profile.messages.all()
        unread_count = message_requests.filter(is_read=False).count()
        context = {
            'message_requests': message_requests,
            'unread_count': unread_count
        }
        return render(request, self.template_name, context)


class MessageView(View):
    template_name = 'message/message.html'

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        message = profile.messages.get(id=kwargs['pk'])
        if message.is_read == False:
            message.is_read = True
            message.save()

        context = {'message': message}
        return render(request, self.template_name, context)


class CreateMessageView(View):
    template_name = 'message/message_form.html'
    form_class = MessageForm

    def setup(self, request, *args, **kwargs):
        try:
            self.sender = request.user.profile
        except:
            self.sender = None
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.recipient = Profile.objects.get(id=kwargs['pk'])

        context = {
            'form': self.form_class,
            'recipient': self.recipient
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = self.sender
            message.recipient = self.recipient
            if self.sender:
                message.name = self.sender.name
                message.email = self.sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('accounts:profile_detail', pk=self.recipient.id)

        context = {
            'form': form,
            'recipient': self.recipient
        }
        return render(request, self.template_name, context)
