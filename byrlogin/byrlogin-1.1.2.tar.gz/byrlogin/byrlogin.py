#!/usr/local/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition
import requests
import sys


def login(studentID,passwd):
    # My API (POST http://10.3.8.211/a11.htm)
    try:
        print "Login in ..."
        r = requests.post(
            url="http://10.3.8.211/a11.htm",
            data = {
                "DDDDD":studentID,
                "upass":passwd,
                "AMKKey":"",
            },
        )
        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        #print('Response HTTP Response Body : {content}'.format(content=r.content))
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')

def logout():
    # My API (2) (GET http://gw.bupt.edu.cn/F.html)
    try:
        print "Login out ..."
        r = requests.get(
            url="http://gw.bupt.edu.cn/F.html",
        )
        print('Response HTTP Status Code : {status_code}'.format(status_code=r.status_code))
        #print('Response HTTP Response Body : {content}'.format(content=r.content))
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')

def main():
    if len(sys.argv) > 1:
        logout()
    else:
        studentID = raw_input("Please Input Your Student ID:")
        hidden = [True] # Nonlocal
        key_bindings_manager = KeyBindingManager()
        @key_bindings_manager.registry.add_binding(Keys.ControlT)
        def _(event):
            hidden[0] = not hidden[0]

        passwd = prompt('Password: ',
                      is_password=Condition(lambda cli: hidden[0]),
                      key_bindings_registry=key_bindings_manager.registry)
        login(studentID,passwd)


if __name__ == '__main__':
    main()


