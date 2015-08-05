'''This is a def for printing the list which is contain in other list'''

def print_lol(the_list):
    '''This def use digui and print every item in the list'''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
