"""这是一个nester模块，定义了一个名为print_lol的函数，这个函数的作用
是用于打印列表，列表中可能包含嵌套列表"""
def print_lol(the_list):
    """这个函数取一个位置参数名为the_list,这可以是任何一个列表，所指定的列表中的每个数据都会输出到屏幕上，各数据占据一行"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
