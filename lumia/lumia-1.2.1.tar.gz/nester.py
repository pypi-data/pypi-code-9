"""下面是列表输出函数"""
import sys
def print_list(the_list, need_tab=False, level=0,file_out=sys.stdout):
    """print list, level is the number of tab symbol"""
    for item in the_list:
        if isinstance(item, list):
            print_list(item, need_tab, level+1, file_out)
        else:
            if need_tab:
                    print("\t"*level,end="",file=file_out)
            print(item,file=file_out)
