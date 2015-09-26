def this(arg1,level):
    for each in arg1:
        if isinstance(each,list):
            this(each,level+1)
        else:
            print(each)
            
