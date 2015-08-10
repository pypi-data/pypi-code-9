"""This is "first_hh"block,it provided a print_lol() function to print list"""
def print_lol(the_list,level=0):
    """this function have a position parameter,which name is the_list,
        every data in the list will print in the screen ,the second parameter
        is used to insert tab"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)
