from django.db import models
from django.db.models.fields import files
from django.forms import ModelForm, fields
from django import forms


from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({ 'class': 'input', 'placeholder': 'Add me' })
        for name, field in self.fields.items():
            field.widget.attrs.update({ 'class': 'input' })

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs.update({ 'class': 'input', 'placeholder': 'Add me' })
        for name, field in self.fields.items():
            field.widget.attrs.update({ 'class': 'input' })