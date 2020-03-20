from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=75)
    username = forms.CharField(max_length=75)
    password = forms.CharField(max_length=75)


class FeedbackForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.EmailField(max_length=200)
