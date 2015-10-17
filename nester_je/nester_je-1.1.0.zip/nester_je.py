"""Python3 practice"""
import nester_je


movies = ["The Holy Grail", 1975,"TerryHones & Terry Gilliam", 91,
          ["Graham Chapman",
           ["Michael Palin","John Cleese","Terry Gilliam",
            "Eric Idle", "Terry Jones"]]]


"""
This is nester.py module, provides one function which is print_lol() function.
"""


def print_lol(the_list, level):
    """This function takes oen positional argument called "the list", which
       is any Python list (of -possibly - nested lists). Each data item in
       the provided list is ( recursively) printed to the screen on it's own
       line."""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t",end="")
            print(each_item)
        
print_lol(movies,0)
