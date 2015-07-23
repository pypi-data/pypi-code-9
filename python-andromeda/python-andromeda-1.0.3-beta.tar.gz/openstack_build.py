__author__ = 'mikelloyd'

import requests
from requests.auth import HTTPBasicAuth
import json
import xml.etree.ElementTree as ET
import os
from xml.etree.ElementTree import ParseError

def GetOpenstackRepos():
    '''
    This will pull the all of the repositories from Github. Currently
    there are ~250 repositories, and Github's API only displays up to
    100 results a page. This will catch all the repositories.

    ..versionadded:: 0.1-beta
    '''
    user = 'kevin.michael.lloyd@gmail.com'
    password = '123qwe!@#QWE'
    url = 'https://api.github.com/orgs/openstack/repos?per_page=100'

    pagination = requests.head(url=url)

    r1 = requests.get(url, auth=HTTPBasicAuth(user, password))
    with open('repos-page-1.json', 'w') as repo:
        repo.write(r1.text)

    next_url = pagination.links['next']['url']
    r2 = requests.get(next_url, auth=HTTPBasicAuth(user, password))
    with open('repos-page-2.json', 'w') as repo:
        repo.write(r2.text)

    final_page = pagination.links['last']['url']
    r3 = requests.get(final_page, auth=HTTPBasicAuth(user, password))
    with open('repos-page-3.json', 'w') as repo:
        repo.write(r3.text)

def GetPath():
    tree = ET.parse('default.xml')
    root = tree.getroot()
    repo1 = open('repos-page-1.json', 'r')
    repo2 = open('repos-page-2.json', 'r')
    repo3 = open('repos-page-3.json', 'r')
    gl_data1 = json.load(repo1)
    gl_data2 = json.load(repo2)
    gl_data3 = json.load(repo3)
    for i in gl_data1:
        for key, value in i.items():
            if key == "full_name":
                print(value)
                child = ET.SubElement(root, 'project')
                print('name=%s' % value)
                child.set('name', value)
                tree.write('default.xml')
    for i in gl_data2:
        for key, value in i.items():
            if key == "full_name":
                print(value)
                child = ET.SubElement(root, 'project')
                print('name=%s' % value)
                child.set('name', value)
                tree.write('default.xml')
    for i in gl_data3:
        for key, value in i.items():
            if key == "full_name":
                print(value)
                child = ET.SubElement(root, 'project')
                print('name=%s' % value)
                child.set('name', value)
                tree.write('default.xml')

def cleanup():
    os.remove('repos-page-1.json')
    os.remove('repos-page-2.json')

GetOpenstackRepos()
GetPath()
# cleanup()
