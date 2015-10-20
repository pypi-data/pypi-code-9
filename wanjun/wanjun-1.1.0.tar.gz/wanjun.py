def checklist(List,indent=False,level=0):
        for i in List:
                if isinstance(i,list):
                        checklist(i,indent,level+1)
                else:
                        if indent:
                                for j in range(level):
                                        print("\t",end='')
                        print(i)

