import json

from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.template import engines
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegistrationForm, LoginForm, AddSwaggerForm
from .services import get_groups, get_accessrules, post_registration, post_login, post_logout, get_group_details, \
    put_groupmodify, post_swagger, get_swagger
from django.contrib import messages
import ast


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
        admin = ast.literal_eval(req.COOKIES['admin'])
    except:
        admin = False
    try:
        authstatus = ast.literal_eval(req.COOKIES['authenticated'])
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
                msg = resp.json()['message']
                messages.info(request, msg, '')
                return redirect('login')
            else:
                token = resp.json()['token']
                admin = resp.json()['admin']
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
    users_lst = None
    if request.method == 'GET':
        try:
            if request.GET['groupname'] != '':
                resp = get_group_details(request.COOKIES['token'], request.GET['groupname'])
                if resp.status_code == 200:
                    users_lst = list(resp.json()['users'])
                else:
                    msg = 'Search failed!'
                    messages.info(request, msg, '')
                    return redirect('group')
        except:
            pass
    elif request.method == 'POST':
        if "Cancel" in request.POST:
            pass
        elif "Save Group" in request.POST:
            lst = request.body.decode('UTF-8').split('&')
            users = []
            for i in range(len(lst) - 1):
                users.append(lst[i].split('=')[1])
            users = [i for i in users if i]
            resp = put_groupmodify(request.COOKIES['token'], request.GET['groupname'], users)
            if resp.status_code != 200:
                msg = resp.json()['message']
                messages.info(request, msg, '')
            else:
                msg = resp.json()
                messages.info(request, msg, '')

    to, ad, au = determine(request)
    return render(request, 'ui/group.html',
                  {'groups': get_groups(request.COOKIES['token']), 'authenticated': au, 'admin': ad,
                   'formset': users_lst})


def access(request):
    to, ad, au = determine(request)
    return render(request, 'ui/access.html',
                  {'accessrules': get_accessrules(request.COOKIES['token']), 'authenticated': au, 'admin': ad})


def dashboard(request):
    to, ad, au = determine(request)
    return render(request, 'ui/dashboard.html', getbody(au, ad))


def logout(request):
    resp = post_logout(request.COOKIES['token'])
    if resp.status_code == 200:
        msg = resp.json()['message']
        messages.info(request, msg, '')
        response = render(request, 'ui/index.html', getbody(False, False))
        response.delete_cookie(key='token')
        response.delete_cookie(key='admin')
        response.delete_cookie(key='authenticated')
        return response
    else:
        msg = 'Something went wrong while logging out'
        messages.info(request, msg, '')
        to, ad, au = determine(request)
        return render(request, 'ui/logout.html', {'authenticated': au, 'admin': ad})


def swaggerview(request):
    to, ad, au = determine(request)
    with open('/Users/aahmed/Documents/FE_GIT/developer_portal/devportal_django_ui/ui/j.json') as json_file:
        abc = json.load(json_file)
    return render(request, 'ui/swagger_embed.html', {'jcon': json.dumps(abc), 'authenticated': au, 'admin': ad})


def swaggeredit(request):
    to, ad, au = determine(request)
    add = False
    edit = False
    form = None
    if request.method == 'GET':
        if "Add" in request.GET:
            add = True
            form = AddSwaggerForm()
        elif "Edit" in request.GET:
            return render(request, 'ui/swaggeredit.html', {'form': form, 'authenticated': au, 'admin': ad,
                                                           'edit': True})
        elif "Search" in request.GET:
            query = 'path=' + request.GET['fname']
            resp = get_swagger(to, query=query)
            if resp.status_code == 200:
                form = AddSwaggerForm(resp.json())
            else:
                msg = resp.json()['message']
                messages.info(request, msg, '')
            return render(request, 'ui/swaggeredit.html', {'form': form, 'authenticated': au, 'admin': ad,
                                                           'edit': True, 'showswag': True})
    elif request.method == 'POST':
        if "Save" in request.POST:
            form = AddSwaggerForm(request.POST)
            if form.is_valid():
                tags = form.cleaned_data['tags'].split(',')
                dependency = form.cleaned_data['dependency'].split(',')
                resp = post_swagger(to, form.cleaned_data['projectname'], form.cleaned_data['path'],
                                    form.cleaned_data['status'], dependency, tags, form.cleaned_data['swaggerobject'])
                if resp.status_code != 200:
                    msg = resp.json()['message']
                    messages.info(request, msg, '')
                    return render(request, 'ui/swaggeredit.html', {'form': form, 'authenticated': au, 'admin': ad,
                                                                   'add': True})
                else:
                    msg = resp.json()
                    messages.info(request, msg, '')
                    return render(request, 'ui/swaggeredit.html', {'authenticated': au, 'admin': ad})
    return render(request, 'ui/swaggeredit.html',
                  {'authenticated': au, 'admin': ad, 'add': add, 'edit': edit, 'form': form})
