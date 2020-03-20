import requests


def get_groups():
    url = "http://127.0.0.1:80/group"
    groupinfo = requests.get(url, headers={'Authorization':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODQ4MDYyNzUsImlhdCI6MTU4NDcxOTg3MCwidXNlciI6ImF0aWYiLCJhZG1pbiI6dHJ1ZX0.ybDwojYGYJQpanKnGxH43T04aVnI7WunsxMmQ-CtKa0'})
    group_list = groupinfo.json()['groupinfo']
    return group_list


def get_accessrules():
    url = "http://127.0.0.1:80/accessrule"
    accessruleinfo = requests.get(url, headers={'Authorization':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODQ4MDYyNzUsImlhdCI6MTU4NDcxOTg3MCwidXNlciI6ImF0aWYiLCJhZG1pbiI6dHJ1ZX0.ybDwojYGYJQpanKnGxH43T04aVnI7WunsxMmQ-CtKa0'})
    accessruleinfo_list = accessruleinfo.json()['accessruleinfo']
    return accessruleinfo_list