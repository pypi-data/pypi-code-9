
'''Shangertest.py can print the essntial elements of a list'''

def print_lol(the_list,level):

    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_level in range(level):
                print('\t',end='')
            print(each_item)


mylist=['Shanger',200,['Shanger',200,['Shanger',200,['Shanger',200,['Shanger',200,['Shanger',200,[]]]]]]]
level_assigned=1
print_lol(mylist,level_assigned)
