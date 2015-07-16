#-*- coding:UTF-8 -*-
#Filename:nester.py
#Authory by : Lyson

#handler list
def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
