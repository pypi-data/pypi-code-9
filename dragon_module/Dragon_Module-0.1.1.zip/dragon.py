#Dragon was created by Dragonkin. All rights reserved!
#Anytime dyn is used, it is referring to the dynamics of the function.
#You need to only import Dragon, and you can add your own files to import with it as well.
#If you will add a new file, put it under "install_requires" in setup.py.
#Designed for Python 2.7.10.
from time import *
from sys import *
from turtle import *
from easygui import *
from random import *

#designed to streamline other functions
def x10(zeroes):
    num = 10 ** zeroes
    return num
def quick_num(dec_places, start, end):
    easy = x10(dec_places)
    start = easy * start
    end = easy * end
    num = randint(start, end) / easy
    return num

#dyn 1 = Float, 2 = Integer, 3 = ?x Float, 4 = ?x Int, 5 = +? Float, 6 = +? Int, None = Float
#dyn 7 = -? Float, 8 = -? Int, 9 = /? Float, /? Int
def rand(start=1, end=10, decimal_places=0, dyn=None, dyn2=None):
    if decimal_places is None:
        if dyn % 2 == 1:
            dyn -= 1
    if dyn == 1 or None:
        num = quick_num(decimal_places, start, end)
    elif dyn == 2:
        num = randint(start, end)
    elif dyn == 3:
        num = quick_num(decimal_places, start, end)
        num = num * dyn2
    elif dyn == 4:
        num = randint(start, end)
        num = num * dyn2
    elif dyn == 5:
        num = quick_num(decimal_places, start, end)
        num += dyn2
    elif dyn == 6:
        num = randint(start, end)
        num += dyn2
    elif dyn == 7:
        num = quick_num(decimal_places, start, end)
        num -= dyn2
    elif dyn == 8:
        num = randint(start, end)
        num -= dyn2
    elif dyn == 9:
        num = quick_num(decimal_places, start, end)
        num = num / dyn2
    elif dyn == 0:
        num = randint(start, end)
        num = num / dyn2
    else:
        num = quick_num(decimal_places, start, end)
    return num

#dyn 0 or None = msgbox, dyn 1 = ynbox, dyn 2 = buttonbox, dyn 3 = ccbox, dyn 4 = indexbox, 
#dyn 5 = enterbox, dyn 6 = intbox, dyn 7 = floatbox
def gui(dyn=None, msg="Error", field1=None, field2=None, field3=None):
    var = None
    while var is None:
        return_field = None
        if msg is None:
            msg = ""
        msg = str(msg)
        if field1 is not None: 
            field1 = str(field1)
        if field2 is not None:
            field2 = str(field2)
        if field3 is not None:
            field3 = str(field3)
        if dyn is None or 0:
            msgbox(msg, ok_button=field1)
            var = ""
        elif dyn == 1:
            var = ynbox(msg)
        elif dyn == 2:
            var = buttonbox(msg, choices=[field1, field2, field3])
        elif dyn == 3:
            var = ccbox(msg)
        elif dyn == 4:
            var = indexbox(msg, choices=[field1, field2, field3])
        elif dyn == 5:
            while var is None:
                var = enterbox(msg)
        elif dyn == 6:
            while var is None:
                var = enterbox(msg)
                try:
                    var = int(var)
                except:
                    var = None
        elif dyn == 7:
            while var is None:
                var = enterbox(msg)
                try:
                    var = float(var)
                except:
                    var = None
            
        if var is not None:
            return var, return_field