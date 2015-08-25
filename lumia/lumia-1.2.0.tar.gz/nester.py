"""下面是列表输出函数"""
def print_list(the_list, need_tab=False, level=0):
    """print list, level is the number of tab symbol"""
    for item in the_list:
        if isinstance(item, list):
            print_list(item, need_tab, level+1)
        else:
            if need_tab:
                    print("\t"*level,end="")
            print(item)
