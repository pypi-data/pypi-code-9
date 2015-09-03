def print_lol(the_list,indent=False,level=0):
    for each_t in the_list:
        if isinstance(each_t,list):
            print_lol(each_t,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='')
            print(each_t)
    
