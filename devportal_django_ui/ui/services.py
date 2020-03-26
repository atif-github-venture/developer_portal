import json

import requests


def get_groups(token):
    url = "http://127.0.0.1:80/group"
    groupinfo = requests.get(url, headers={
        'Authorization': token})
    group_list = groupinfo.json()['groupinfo']
    return group_list


def get_accessrules(token):
    url = "http://127.0.0.1:80/accessrule"
    accessruleinfo = requests.get(url, headers={
        'Authorization': token})
    accessruleinfo_list = accessruleinfo.json()['accessruleinfo']
    return accessruleinfo_list


def get_group_details(token, searchstr):
    url = "http://127.0.0.1:80/group/" + searchstr
    resp = requests.get(url, headers={
        'Authorization': token})
    return resp


def post_registration(email, user, password):
    url = "http://127.0.0.1:80/user"
    payload = {
        'email': email,
        'username': user,
        'password': password
    }
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url, data=json.dumps(payload), headers=headers)
    resp.close()
    msg = resp.json()['message']
    return msg


def post_login(email, password):
    url = "http://127.0.0.1:80/auth/login"
    payload = {
        'email': email,
        'password': password
    }
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url, data=json.dumps(payload), headers=headers)
    resp.close()
    return resp


def put_groupmodify(token, searchstr, userlist):
    url = "http://127.0.0.1:80/group/" + searchstr
    payload = {
        'groupname': searchstr,
        'users': userlist
    }
    resp = requests.put(url, data=json.dumps(payload), headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def get_swagger(token, query):
    url = "http://127.0.0.1:80/swagger?" + query
    resp = requests.get(url, headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def post_swagger(token, projname, path, status, dep, tags, swagobj):
    url = "http://127.0.0.1:80/swagger"
    payload = {
        "projectname": projname,
        "path": path,
        "tags": tags,
        "status": status,
        "swaggerobject": swagobj,
        "dependency": dep
    }
    resp = requests.post(url, data=json.dumps(payload), headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def put_swagger(token, projname, path, status, dep, tags, swagobj):
    url = "http://127.0.0.1:80/swagger/edit?path=" + path
    payload = {
        "projectname": projname,
        "path": path,
        "tags": tags,
        "status": status,
        "swaggerobject": swagobj,
        "dependency": dep
    }
    resp = requests.put(url, data=json.dumps(payload), headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def post_logout(token):
    url = "http://127.0.0.1:80/auth/logout"
    headers = {'Authorization': token}
    resp = requests.post(url, data=None, headers=headers)
    resp.close()
    return resp
