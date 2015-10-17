"""Python3 practice"""

movies = ["The Holy Grail", 1975,"TerryHones & Terry Gilliam", 91,
          ["Graham Chapman",
           ["Michael Palin","John Cleese","Terry Gilliam",
            "Eric Idle", "Terry Jones"]]]

"""
This is nester.py module, provides one function which is print_lol() function.
"""


def print_lol(the_list):
    """This function takes oen positional argument called "the list", which
       is any Python list (of -possibly - nested lists). Each data item in
       the provided list is ( recursively) printed to the screen on it's own
       line."""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
        
print_lol(movies)
