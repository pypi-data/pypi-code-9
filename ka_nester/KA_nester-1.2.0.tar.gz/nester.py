from __future__ import print_function

### Prints nested lists into lists
def print_lol(the_list, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end=' ')
            print(each_item)

