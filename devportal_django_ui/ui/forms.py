from django import forms
# from taggit.managers import TaggableManager
from django.forms import formset_factory

STATUS = [
    ('Published', 'Published'),
    ('Deployed', 'Deployed'),
    ('Deprecated', 'Deprecated'),
]

class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=200)
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class AddSwaggerForm(forms.Form):
    projectname = forms.CharField(max_length=100, label='Project Name')
    path = forms.CharField(max_length=200, label='Path')
    status = forms.ChoiceField(widget=forms.RadioSelect, choices=STATUS, label='Status')
    tags = forms.CharField(max_length=200, label='Tags')
    dependency = forms.CharField(max_length=200, label='Dependency')
    swaggerobject = forms.CharField(widget=forms.Textarea, label='Swagger JSON')