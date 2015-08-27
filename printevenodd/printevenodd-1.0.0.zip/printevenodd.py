__author__ = 'sergey.meerovich'
"""This module have to simple functions that handle lists and strings \
   that means it can print even , or odd characters on strings and  \
   print each even or odd element in a list
   functions names print_even(tested_string_name) to print even values
   fuctions names print_odd(tested_string_name)  to print odd values
   module created by Sergey Meerovich
"""
def print_even(tested_list):
   length=len(tested_list)
   for i in range(0,length,1):
          if(i%2==0):
             print(tested_list[i])
          else:
              pass

def print_odd(tested_list):
   length=len(tested_list)
   for i in range(0,length,1):
       if(i%2!=0):
          print(tested_list[i])
       else:
           pass
