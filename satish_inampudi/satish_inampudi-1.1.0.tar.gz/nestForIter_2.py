def nestForIter(thisList, indent=False, level=0):
    for each in thisList:
        if isinstance(each,list):
            nestForIter(each,indent,level+1)
        else:
            if(indent):
                for val in range(level):
                    print("\t",end='')
            print(each)
            
