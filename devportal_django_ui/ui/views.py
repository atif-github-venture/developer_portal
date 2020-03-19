from django.shortcuts import render
from django.template import engines


# # from django.template.loader import render_to_string

# Create your views here.


def base(request):
    return render(request, 'ui/base.html')


def register(request):
    return render(request, 'ui/registration.html')

def index(request):
    return render(request, 'ui/index.html')

def login(request):
    return render(request, 'ui/login.html')

def about(request):
    django_engine = engines['django']
    return render(request, django_engine.from_string('login.html').render({'title': 'Dev Portal', 'author': 'Atif'}))
