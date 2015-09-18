"""movies=["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,
        ["Graham Chapman",["Michael Palin","John Cleese","Terry Gilliam",
                           "Eric Idle","Terry Jones"]]]"""

"""this is a test module write from John"""
def recujohnlist(movies,indent=False,level=0):
    """this function can print all things in your list"""
    for each_item in movies:
        if isinstance(each_item,list):
            recujohnlist(each_item,indent,level+1)
        else:
            if indent:
                for s in range(level):
                    print('\t',end='')
            print(each_item)
