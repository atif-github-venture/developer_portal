import json
import requests
from django.conf import settings


RESTHOST = getattr(settings, "RESTHOST", None)


def get_groups(token):
    url = "http://" + RESTHOST + "/group"
    groupinfo = requests.get(url, headers={
        'Authorization': token})
    group_list = groupinfo.json()['groupinfo']
    return group_list


def get_accessrules(token):
    url = "http://" + RESTHOST + "/accessrule"
    accessruleinfo = requests.get(url, headers={
        'Authorization': token})
    accessruleinfo_list = accessruleinfo.json()['accessruleinfo']
    return accessruleinfo_list


def get_group_details(token, searchstr):
    url = "http://" + RESTHOST + "/group/" + searchstr
    resp = requests.get(url, headers={
        'Authorization': token})
    return resp


def post_registration(email, user, password):
    url = "http://" + RESTHOST + "/user"
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
    url = "http://" + RESTHOST + "/auth/login"
    payload = {
        'username': email,
        'password': password
    }
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url, data=json.dumps(payload), headers=headers)
    resp.close()
    return resp


def put_groupmodify(token, searchstr, userlist):
    url = "http://" + RESTHOST + "/group/" + searchstr
    payload = {
        'groupname': searchstr,
        'users': userlist
    }
    resp = requests.put(url, data=json.dumps(payload), headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def get_swaggerprojects(token):
    url = "http://" + RESTHOST + "/swagger/project"
    resp = requests.get(url, headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def get_swaggerlist(token, search):
    url = "http://" + RESTHOST + "/swagger/project/"+search
    resp = requests.get(url, headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def get_permission(token):
    url = "http://" + RESTHOST + "/permission"
    resp = requests.get(url, headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def post_permission(token, user, listofperm):
    url = "http://" + RESTHOST + "/permission"
    payload = {
        "user": user,
        "permission": listofperm
    }
    resp = requests.post(url, data=json.dumps(payload), headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def put_permission(token, user, listofperm):
    url = "http://" + RESTHOST + "/permission"
    payload = {
        "user": user,
        "permission": listofperm
    }
    resp = requests.put(url, data=json.dumps(payload), headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def get_users(token):
    url = "http://" + RESTHOST + "/user"
    resp = requests.get(url, headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def get_swagger_metrics(token):
    url = "http://" + RESTHOST + "/swagger/metrics"
    resp = requests.get(url, headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def get_swagger(token, query):
    url = "http://" + RESTHOST + "/swagger?" + query
    resp = requests.get(url, headers={
        'Authorization': token, 'Content-Type': 'application/json'})
    return resp


def post_swagger(token, projname, path, status, dep, tags, swagobj):
    url = "http://" + RESTHOST + "/swagger"
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
    url = "http://" + RESTHOST + "/swagger/edit?path=" + path
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
    url = "http://" + RESTHOST + "/auth/logout"
    headers = {'Authorization': token}
    resp = requests.post(url, data=None, headers=headers)
    resp.close()
    return resp
