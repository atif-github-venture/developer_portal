from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=200)
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200)
    password = forms.CharField(max_length=200)
