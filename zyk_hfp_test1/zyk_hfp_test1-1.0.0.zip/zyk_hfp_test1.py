""" This is noly a test1 from head first pyhton"""

def print_lol(the_list) :
    for each_item in the_list :
        if isinstance(each_item, list) :
            print_lol(each_item)
        else:
            print (each_item)
