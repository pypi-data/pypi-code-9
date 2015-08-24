"""下面是列表输出函数"""
def print_list(the_list):
    """利用递归进行列表的输出"""
    for item in the_list:
        if isinstance(item, list):
            print_list(item)
        else:
            print(item)