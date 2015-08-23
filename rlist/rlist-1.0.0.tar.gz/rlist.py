""" The 1st python program by QS Chou
>>> a r_plist function is defined, it will recursively to read the nested list
>>> and print the cell in the list.
>>> it will also take an indent by tab; thus will print the content in more structural manner """

""" Learning from the function;
1. Build in Function (BIF)
    isinstance, range
2. List, nested list
3. Recursive method
4. argument, rquired argument, optional argument (default value is assigned)"""

def r_plist(the_list,indent=False, level=0):
    for e in the_list:
        if isinstance(e,list):
            r_plist(e,indent,level+1)
        else:
            if indent:
                for tab_ind in range(level):
                    print("\t",end='')
            # -- The range method could be replaced by the more elegant code#
            #print ("\t"*level,end='')
            print(e)



