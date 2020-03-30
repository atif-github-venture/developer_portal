import json

from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.template import engines
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RegistrationForm, LoginForm, AddSwaggerForm, PermissionForm
from .services import get_groups, get_accessrules, post_registration, post_login, post_logout, get_group_details, \
    put_groupmodify, post_swagger, get_swagger, put_swagger, get_permission, get_users, post_permission, put_permission, \
    get_swaggerprojects, get_swaggerlist
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


def dependency(request):
    to, ad, au = determine(request)
    return render(request, 'ui/dependency.html', getbody(au, ad))


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
    return render(request, 'ui/register.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            resp = post_login(form.cleaned_data['username'], form.cleaned_data['password'])
            if resp.status_code != 200:
                msg = resp.json()['message']
                messages.info(request, msg, '')
                return redirect('signin')
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
            return redirect('signin')
    else:
        form = LoginForm()
    return render(request, 'ui/signin.html', {'form': form})


# def group(request):
#     users_lst = None
#     if request.method == 'GET':
#         try:
#             if request.GET['groupname'] != '':
#                 resp = get_group_details(request.COOKIES['token'], request.GET['groupname'])
#                 if resp.status_code == 200:
#                     users_lst = list(resp.json()['users'])
#                 else:
#                     msg = 'Search failed!'
#                     messages.info(request, msg, '')
#                     return redirect('group')
#         except:
#             pass
#     elif request.method == 'POST':
#         if "Cancel" in request.POST:
#             pass
#         elif "Save Group" in request.POST:
#             lst = request.body.decode('UTF-8').split('&')
#             users = []
#             for i in range(len(lst) - 1):
#                 users.append(lst[i].split('=')[1])
#             users = [i for i in users if i]
#             resp = put_groupmodify(request.COOKIES['token'], request.GET['groupname'], users)
#             if resp.status_code != 200:
#                 msg = resp.json()['message']
#                 messages.info(request, msg, '')
#             else:
#                 msg = resp.json()
#                 messages.info(request, msg, '')
#
#     to, ad, au = determine(request)
#     return render(request, 'ui/group.html',
#                   {'groups': get_groups(request.COOKIES['token']), 'authenticated': au, 'admin': ad,
#                    'formset': users_lst})


def admin(request):
    form = None
    to, ad, au = determine(request)
    users_resp = get_users(to)
    perm = None
    if users_resp.status_code == 200:
        users = [item['username'] for item in users_resp.json()['data']]
    else:
        msg = 'Search failed!'
        messages.info(request, msg, '')
        return redirect('admin')
    if request.method == 'GET':
        # form = PermissionForm()
        perm_resp = get_permission(to)
        if perm_resp.status_code == 200:
            perm = perm_resp.json()
        else:
            msg = 'Search failed!'
            messages.info(request, msg, '')
            return redirect('admin')

        return render(request, 'ui/admin.html',
                      {'form': form, 'users': users, 'authenticated': au, 'admin': ad, 'perm': perm})
    elif request.method == 'POST':
        if 'adduserperm' in request.POST:
            permlist = []
            try:
                permlist.append(request.POST['admin'].lower())
            except:
                pass
            try:
                permlist.append(request.POST['developer'].lower())
            except:
                pass
            try:
                permlist.append(request.POST['view'].lower())
            except:
                pass
            resp = post_permission(to, request.POST['userlist'], permlist)
            if resp.status_code == 200:
                msg = resp.json()
            else:
                msg = resp.json()['message']
            messages.info(request, msg, '')
        elif 'modifyuserperm' in request.POST:
            user = request.POST['modifyuserperm'].lower()
            permlist = []
            try:
                permlist.append(request.POST['admin'].lower().replace('_' + user, ''))
            except:
                pass
            try:
                permlist.append(request.POST['developer'].lower().replace('_' + user, ''))
            except:
                pass
            try:
                permlist.append(request.POST['view'].lower().replace('_' + user, ''))
            except:
                pass
            resp = put_permission(to, user, permlist)
            if resp.status_code == 200:
                msg = resp.json()
            else:
                msg = resp.json()['message']
            messages.info(request, msg, '')

    return redirect('admin')


def dashboard(request):
    from plotly.offline import plot
    from plotly.graph_objs import Scatter
    to, ad, au = determine(request)
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    plot_div = plot([Scatter(x=x_data, y=y_data,
                             mode='lines', name='test',
                             opacity=0.8, marker_color='green')],
                    output_type='div')
    return render(request, 'ui/dashboard.html', {'authenticated': au, 'admin': ad, 'plot_div': plot_div})


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
        response = render(request, 'ui/index.html', getbody(False, False))
        response.delete_cookie(key='token')
        response.delete_cookie(key='admin')
        response.delete_cookie(key='authenticated')
        return response


def swaggerview(request):
    to, ad, au = determine(request)
    projects = get_swaggerprojects(to)
    projname = None
    path_list = None
    selectedpath = None
    swagobj = None
    if request.method == 'GET':
        if 'getapipath' in request.GET:
            projname = request.GET['projectlist']
            resp = get_swaggerlist(to, projname)
            if resp.status_code == 200:
                path_list = resp.json()
            else:
                messages.info(request, 'Invalid search!', '')
        if 'getswagger' in request.GET:
            path_list = request.GET['getswagger'].split(';')[1:]
            projname = request.GET['projectlist']
            selectedpath = request.GET['pathlist']
            query = 'path=' + selectedpath
            resp = get_swagger(to, query=query)
            if resp.status_code == 200:
                swagobj = resp.json()['swaggerobject']
            else:
                messages.info(request, 'Invalid result!', '')
        return render(request, 'ui/swagger_embed.html',
                      {'authenticated': au, 'admin': ad, 'projects': projects.json(),
                       'paths': path_list, 'projname': projname, 'jcon': swagobj, 'selectedpath': selectedpath})

    # with open('/Users/aahmed/Documents/FE_GIT/developer_portal/devportal_django_ui/ui/j.json') as json_file:
    #     abc = json.load(json_file)
    # return render(request, 'ui/swagger_embed.html',
    #               {'jcon': json.dumps('abc'), 'authenticated': au, 'admin': ad, 'projects': projects.json(),
    #                'path': path.json()})


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
                load = {
                    'projectname': resp.json()['projectname'],
                    'path': resp.json()['path'],
                    'tags': ','.join(resp.json()['tags']),
                    'status': resp.json()['status'],
                    'dependency': ','.join(resp.json()['dependency']),
                    'swaggerobject': resp.json()['swaggerobject'],
                }
                form = AddSwaggerForm(load)
                showtag = True
            else:
                messages.info(request, 'Invalid search!', '')
                showtag = False
            return render(request, 'ui/swaggeredit.html', {'form': form, 'authenticated': au, 'admin': ad,
                                                           'edit': True, 'showswag': showtag})
    elif request.method == 'POST':
        if "Save" in request.POST:
            form = AddSwaggerForm(request.POST)
            if form.is_valid():
                tags = form.cleaned_data['tags'].replace(' ', '').split(',')
                dependency = form.cleaned_data['dependency'].replace(' ', '').split(',')
                try:
                    # /modification
                    if request.GET['fname'] is not None:
                        resp = put_swagger(to, form.cleaned_data['projectname'], form.cleaned_data['path'],
                                           form.cleaned_data['status'], dependency, tags,
                                           form.cleaned_data['swaggerobject'])
                except:
                    # /adding
                    resp = post_swagger(to, form.cleaned_data['projectname'], form.cleaned_data['path'],
                                        form.cleaned_data['status'], dependency, tags,
                                        form.cleaned_data['swaggerobject'])
                if resp.status_code != 200:
                    if resp.status_code == 404:
                        msg = 'Search criteria not found'
                    else:
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
