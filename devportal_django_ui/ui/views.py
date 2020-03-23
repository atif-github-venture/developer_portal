from django.shortcuts import render, redirect
from django.template import engines
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegistrationForm, LoginForm
from .services import get_groups, get_accessrules, post_registration, post_login, post_logout
from django.contrib import messages


def getbody(auth, adm):
    return {
        'authenticated': auth,
        'admin': adm
    }


def determine(req):
    try:
        token = req.COOKIES['token']
    except:
        token = None
    try:
        admin = bool(req.COOKIES['admin'])
    except:
        admin = False
    try:
        authstatus = bool(req.COOKIES['authenticated'])
    except:
        authstatus = False
    return token, admin, authstatus


def index(request):
    to, ad, au = determine(request)
    return render(request, 'ui/index.html', getbody(au, ad))


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


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            resp = post_login(form.cleaned_data['email'], form.cleaned_data['password'])
            if resp.status_code != 200:
                msg = 'Message: ' + resp.json()['message']
                messages.info(request, msg, '')
                return redirect('login')
            else:
                token = resp.json()['token']
                admin = bool(resp.json()['admin'])
                messages.info(request, 'You have successfully logged in!', '')
                response = render(request, 'ui/dashboard.html', getbody(True, admin))
                response.set_cookie(key='token', value=token)
                response.set_cookie(key='admin', value=admin)
                response.set_cookie(key='authenticated', value=True)
                return response
        else:
            return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'ui/login.html', {'form': form})


def group(request):
    to, ad, au = determine(request)
    return render(request, 'ui/group.html', {'groups': get_groups(request.COOKIES['token']), 'authenticated': au, 'admin': ad})


def access(request):
    to, ad, au = determine(request)
    return render(request, 'ui/access.html', {'accessrules': get_accessrules(request.COOKIES['token']), 'authenticated': au, 'admin': ad})


def dashboard(request):
    to, ad, au = determine(request)
    return render(request, 'ui/dashboard.html', getbody(au, ad))


def logout(request):
    resp = post_logout(request.COOKIES['token'])
    if resp.status_code == 200:
        msg = 'Message: ' + resp.json()['message']
        messages.info(request, msg, '')
        response = render(request, 'ui/index.html', getbody(False, False))
        response.delete_cookie(key='token')
        response.delete_cookie(key='admin')
        response.delete_cookie(key='authenticated')
        return response
    else:
        msg = 'Message: Something went wrong while logging out'
        messages.info(request, msg, '')
        to, ad, au = determine(request)
        return render(request, 'ui/logout.html', {'authenticated': au, 'admin': ad})
