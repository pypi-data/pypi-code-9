"""movies=["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,
        ["Graham Chapman",["Michael Palin","John Cleese","Terry Gilliam",
                           "Eric Idle","Terry Jones"]]]"""

"""this is a test module write from John"""
def recujohnlist(movies):
    """this function can print all things in your list"""
    for each_item in movies:
        if isinstance(each_item,list):
            recujohnlist(each_item)
        else:
            print(each_item)


