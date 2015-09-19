__author__ = 'user'
# coding=utf-8
#nester_effy_zhao.py
import sys
""" hello,this is a recursive function to print each item in ths list"""
def func_rec(arg,ident=False,level=0):
    for item in arg:
       if  isinstance(arg,list):
            func_rec(item,ident,level+1)
       else:
            if ident:
                for i in range(level):
                    print ' ',
            print item
