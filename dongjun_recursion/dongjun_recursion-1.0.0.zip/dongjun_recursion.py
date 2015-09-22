'''通过递归来将一个列表的所有项输出出来,并且根据项目所在列表级别不同添加不同个数的制表符'''

def print_item(the_list,indent,level):
    for i in the_list:
        if isinstance(i,list):
            print_item(i,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='')
            print(i)
