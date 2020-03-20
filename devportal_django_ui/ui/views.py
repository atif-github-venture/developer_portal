from django.shortcuts import render, redirect
from django.template import engines
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import GroupForm
from .services import get_groups, get_accessrules


# # from django.template.loader import render_to_string

# Create your views here.


def base(request):
    return render(request, 'ui/base.html')


def index(request):
    return render(request, 'ui/index.html')


def register(request):
    return render(request, 'ui/registration.html')


def group(request):
    if request.method == 'POST':
        f = GroupForm(request.POST)

        if f.is_valid():
            name = f.cleaned_data['name']
            sender = f.cleaned_data['email']
            subject = "You have a new Feedback from {}:{}".format(name, sender)
            message = "Subject: {}\n\nMessage: {}".format(f.cleaned_data['subject'], f.cleaned_data['message'])
            # mail_admins(subject, message)

            f.save()
            # messages.add_message(request, messages.INFO, 'Feedback Submitted.')
            return redirect('group')
    else:
        context = {
            'groups': get_groups(),
        }
    return render(request, 'ui/group.html', {'groups': get_groups()})


def access(request):
    return render(request, 'ui/access.html', {'accessrules': get_accessrules()})


def logout(request):
    # logout(request)
    return HttpResponseRedirect(reverse('base'))


# @login_required
def login(request):
    return render(request, 'ui/login.html')

# def about(request):
#     django_engine = engines['django']
#     return render(request, django_engine.from_string('login.html').render({'title': 'Dev Portal', 'author': 'Atif'}))
