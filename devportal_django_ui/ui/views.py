from django.shortcuts import render, redirect
from django.template import engines
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import RegistrationForm, LoginForm
from .services import get_groups, get_accessrules, post_registration, post_login
from django.contrib import messages


def base(request):
    return render(request, 'ui/base.html')


def index(request):
    return render(request, 'ui/index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            msg = post_registration(form.cleaned_data['email'], form.cleaned_data['username'],
                                    form.cleaned_data['password'])
            messages.info(request, msg)
            return redirect('register')
    else:
        form = RegistrationForm()
    return render(request, 'ui/registration.html', {'form': form})


# @login_required
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            msg = post_login(form.cleaned_data['email'], form.cleaned_data['password'])
            if msg != None:
                messages.info(request, msg, '')
                return redirect('login')
            return render(request, 'ui/dashboard.html')
    else:
        form = LoginForm()
    return render(request, 'ui/login.html', {'form': form})


def group(request):
    return render(request, 'ui/group.html', {'groups': get_groups()})


def access(request):
    return render(request, 'ui/access.html', {'accessrules': get_accessrules()})


def dashboard(request):
    return render(request, 'ui/dashboard.html')


def logout(request):
    # logout(request)
    return HttpResponseRedirect(reverse('base'))

# def about(request):
#     django_engine = engines['django']
#     return render(request, django_engine.from_string('login.html').render({'title': 'Dev Portal', 'author': 'Atif'}))
