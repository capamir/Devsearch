from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.core.exceptions import ValidationError

from .models import User, Profile, Skill, Message


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'username', 'password1', 'password2')
        labels = {'first_name': 'Name'}

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists')
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'email', 'username',
                  'location', 'bio', 'short_intro', 'image',
                  'social_github', 'social_linkedin', 'social_twitter',
                  'social_youtube', 'social_website')


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ('owner',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
