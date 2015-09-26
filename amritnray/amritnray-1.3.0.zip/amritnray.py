def this(arg1,indent=False,level=0):
    for each in arg1:
        if isinstance(each,list):
            this(each,indent,level+1)
        else:
            if indent:
            for tab_stop in range(leve):
                print("\t",end='')
             print(each)   
                      
            
