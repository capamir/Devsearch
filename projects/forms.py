from django import forms

from .models import Project, Review


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'image', 'description',
                  'demo_link', 'source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }
