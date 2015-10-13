#movie=['The Holy Grail',1975,'Terry Jones & Terry Gilliam','91',['Graham Chapman',['Michael Palin',
#         'John Cleese','Terry Gilliam','Eric Idle','Terry Jones']]]
"""This program is wrrte by kain wu"""
def print_lol(the_list,level=0):
    """This function is to print a list even thought it is with list in list"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            print("\t"*level,end='')
        print(each_item)
            

