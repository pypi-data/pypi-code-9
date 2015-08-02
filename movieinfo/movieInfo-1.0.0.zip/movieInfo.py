"""Ihe function is to print the elements of the list . Even the list has many sub
 lists, it will print every element of the sublist instead of a list"""
def movieInfo(theList):
    for items in theList:
        if not isinstance(items,list):
                print items
        else:
                movieInfo(items)
