from django import forms
from django.forms import formset_factory


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=200)
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

