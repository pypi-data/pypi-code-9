#!/usr/bin/env python
#encoding:utf-8
"""
this is the "nester.py" module and it provides one function called print_lol()
"""
def print_lol(the_list):
    for item_list in the_list:
        if isinstance(item_list,list):
            print (item_list)
        else:
            print(item_list)
