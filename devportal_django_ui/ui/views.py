from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, AddSwaggerForm
from .services import post_registration, post_login, post_logout, \
    post_swagger, get_swagger, put_swagger, get_permission, get_users, post_permission, put_permission, \
    get_swaggerprojects, get_swaggerlist, get_swagger_metrics
from django.contrib import messages
import ast
import plotly.graph_objects as go
from plotly.offline import plot


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


def home(request):
    to, ad, au = determine(request)
    return render(request, 'ui/home.html', getbody(au, ad))


def dependency(request):
    to, ad, au = determine(request)
    from graphviz import Digraph
    dot = Digraph(comment='Service Dependencies', format='svg')
    dot.node('A', 'Login')
    dot.node('B', 'Accounts')
    dot.node('C', 'Collections')
    dot.node('D', 'Products')
    dot.edges(['AB', 'AD', 'AC', 'CD'])
    dot.edge('B', 'D', constraint='false')
    dot.edge('B', 'C', constraint='false')
    d_s = dot.pipe().decode('utf-8')

    from pyvis.network import Network
    import pandas as pd

    got_net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # set the physics layout of the network
    got_net.barnes_hut()

    sources = ['Login','Login', 'Login', 'Login', 'Collection', 'Product']
    targets = ['Account', 'Product', 'Collection', 'Checkout', 'Product', 'Checkout']
    weights = [30, 30, 30, 30, 30, 30]

    edge_data = zip(sources, targets, weights)

    for e in edge_data:
        src = e[0]
        dst = e[1]
        w = e[2]

        got_net.add_node(src, src, title=src)
        got_net.add_node(dst, dst, title=dst)
        got_net.add_edge(src, dst, value=w)

    neighbor_map = got_net.get_adj_list()

    # add neighbor data to node hover data
    for node in got_net.nodes:
        node["title"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
        node["value"] = len(neighbor_map[node["id"]])
    # got_net.show_buttons(filter_=['physics'])
    got_net.set_options("""var options = {
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -23577,
          "centralGravity": 4.95,
          "springLength": 260,
          "springConstant": 0.44,
          "damping": 0.14,
          "avoidOverlap": 0.46
        },
        "maxVelocity": 118,
        "minVelocity": 0.2,
        "timestep": 0.11
      }
    }""")
    got_net.write_html("ui/dep.html")
    import codecs
    f = codecs.open("ui/dep.html", 'r', 'utf-8')
    d_s1 = f.read()
    f.close()
    import os
    os.remove("ui/dep.html")
    return render(request, 'ui/dependency.html', {'authenticated': au, 'admin': ad, 'd_s': d_s, 'd_s1': d_s1})



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
    to, ad, au = determine(request)
    plot_div = None
    plot_div_pie = None
    resp = get_swagger_metrics(to)
    if resp.status_code == 200:
        items = resp.json()
        status = items['status']
        data = []
        for item in items['project_list']:
            data.append(
                go.Bar(
                    x=status,
                    y=item['status_count'],
                    name=item['project']
                )
            )
        fig = go.Figure(data=data, layout={'template': 'plotly_dark'})
        fig.update_layout(barmode='group', showlegend=True, title="API Documentation per Project",
                          xaxis_title="Lifecycle Status",
                          yaxis_title="Count")
        plot_div = plot(fig, output_type='div')

        stat_values = items['status_count_overall']
        fig_pie = go.Figure(data=[go.Pie(labels=status, values=stat_values, pull=[0, 0, 0.2, 0])],
                            layout={'template': 'plotly_dark'})
        fig_pie.update_layout(showlegend=True, title="Overall Lifecycle Status")
        plot_div_pie = plot(fig_pie, output_type='div')
    else:
        messages.info(request, 'Something went wrong at server level', '')
    return render(request, 'ui/dashboard.html',
                  {'authenticated': au, 'admin': ad, 'plot_div': plot_div, 'plot_div_pie': plot_div_pie})


def logout(request):
    resp = post_logout(request.COOKIES['token'])
    if resp.status_code == 200:
        msg = resp.json()['message']
        messages.info(request, msg, '')
        response = render(request, 'ui/home.html', getbody(False, False))
        response.delete_cookie(key='token')
        response.delete_cookie(key='admin')
        response.delete_cookie(key='authenticated')
        return response
    else:
        msg = 'Something went wrong while logging out'
        messages.info(request, msg, '')
        response = render(request, 'ui/home.html', getbody(False, False))
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
    if projects.status_code == 200:
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
    else:
        messages.info(request, projects.json()['message'], '')
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
                messages.info(request, 'Its an invalid search or authorization failure!', '')
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
