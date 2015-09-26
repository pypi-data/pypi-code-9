def this(arg1,level=0):
    for each in arg1:
        if isinstance(each,list):
            this(each,level+1)
        else:
            for tab_stop in range(leve):
                print("\t",end='')
             print(each)   
                      
            
