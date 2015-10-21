"""
  This is simple nested module, provided a function 'print_lol()'.
  it will print item of lists, whether that list included nested list or not.
"""
import sys

def print_lol(the_list,
              indent = False,
              level = 0,
              fh = sys.stdout):
    """
    the_list - any python list.
    indent - set for indentation.
    level - indent for nested list.
    fh - set print out destination, default - [sys.stdout].
    """
    if level < 0:
        indent = False
    for each_item in the_list:
        if isinstance(each_item,list):         
            print_lol(each_item, indent, level+1, fh)
        else:
            if indent:
                for tap_stop in range(level):
                    print("\t",end='',file = fh)
            print(each_item, file = fh)

