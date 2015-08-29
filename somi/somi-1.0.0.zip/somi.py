def pirnt_lol(the_list,indent=False,level=0,fn=sys.stdout):
    for each_list in the_list:
        if isinstance(each_list,list):
            print_lol(each_list,indent,level+1,fn)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='',file=fn)
                print(each_list,file=fn)
                
