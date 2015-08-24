def print_lol (the_list,ident=False,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,ident,level+1)
        else:
            
                for tap_stop in range(level):
                    if ident:
                     print('\t',end='')
                print(each_item)
            

     
