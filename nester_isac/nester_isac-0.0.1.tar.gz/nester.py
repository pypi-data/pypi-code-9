#!/usr/env/python3
#encoding: utf-8

'''Module with functionalities about handle data list '''

def print_lol(items):
    '''Print datas within the list. Whether 
    data item is a list, so print_lol is called
    recursivelly '''

    for item in items:
        if isinstance(item, list):
            print_lol(item)
        else:
            print(item)
