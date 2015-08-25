"""下面是列表输出函数"""
def print_list(the_list, level=0):
    """利用递归进行列表的输出,level is the number of tab symbol"""
    for item in the_list:
        if isinstance(item, list):
            print_list(item,level+1)
        else:
            for num in range(level):
                print("\t",end="")
            print(item)
