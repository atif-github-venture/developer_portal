from django import forms


STATUS = [
    ('Published', 'Published'),
    ('Deployed', 'Deployed'),
    ('Deprecated', 'Deprecated'),
]

PERMISSION = [
    ('Admin', 'Admin'),
    ('Developer', 'Developer'),
    ('View', 'View'),
]


class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Email address', max_length=200,
                             widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-control'}))
    username = forms.CharField(label='User Name', max_length=32,
                               widget=forms.TextInput(attrs={'placeholder': 'User Name', 'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=32,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=200,
                             widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(label='Password', max_length=32,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))


class AddSwaggerForm(forms.Form):
    projectname = forms.CharField(max_length=100, label='Project Name')
    path = forms.CharField(max_length=200, label='Path')
    status = forms.ChoiceField(widget=forms.RadioSelect, choices=STATUS, label='Status')
    tags = forms.CharField(max_length=200, label='Tags')
    dependency = forms.CharField(max_length=200, label='Dependency')
    swaggerobject = forms.CharField(widget=forms.Textarea, label='Swagger JSON')


class PermissionForm(forms.Form):
    user = forms.CharField(max_length=200,
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    permission = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=PERMISSION,
    )