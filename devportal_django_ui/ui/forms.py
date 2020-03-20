from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(max_length=75, help_text="Name of the sender")
    username = forms.CharField(max_length=75)
    password = forms.CharField(max_length=75)
