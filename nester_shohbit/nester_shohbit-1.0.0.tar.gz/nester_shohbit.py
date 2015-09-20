
def funcMovie(a_list,tabify = False,level=0):
        for each_item in a_list:
                if isinstance(each_item,list):
                        funcMovie(each_item,tabify,level+1)
                else :
                        if(tabify):
                                for tab_stop in range(level):
                                        print("\t", end='')
                        
                        print(each_item)
                        
