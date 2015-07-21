def print_list(list_name,tab_count=0):
    for each_item in list_name:
        if isinstance(each_item,list):
            print_list(each_item,tab_count+1)
        else:
            for tab_num in range(tab_count):
                print("\t",end="")
            print(each_item)            
    print("=====The End======")

def print_string():
    for count in range(3):
        print("Never give up!!!")


				
