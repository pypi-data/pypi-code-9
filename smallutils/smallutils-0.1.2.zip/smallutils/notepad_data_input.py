"""
    Module to allow users to enter info to notepad and pgrm retrieve contents from notepad. 

"""
import os, re, sys
from start_prgm_handler import spawn_program


def read_data_fr_file(filename): 
    """ Read all parameters from a file. Empty line and those with comment '#' will be ignored.
        Args:
            filename (str): full path of input.func_closure
        Returns:
            (list): list of contents.
    """
    
    with open(filename,'r') as f:
        included_para = [x.split('\n')[0] for x in f.readlines()]
        included_para = [x for x in included_para if x!=''and not re.search('^\#.*',x)]#add the # key to the search

    return included_para

def read_data_fr_notepad(working_file, clear_content_first = 0):
    """ Function to open note pad and allow user to input the data and return the data recorded upon closing
        Args:
            working_file (str): full path of the notepad txt.
        kwargs:
            clear_content_first (binary): default 0. If 1, will clear the contents.
        Returns:
            (list): list of the data. Return those without comment '#' or empty space.
    """
    if not working_file:
        print "Enter a valid file to store the notepad txt"
        raise

    #check if not file exist --> create the file and ensure dir is present
    if not os.path.isfile(working_file):
        basedir = os.path.dirname(working_file)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
            
        open(working_file, 'w').close()

    if clear_content_first:
        with open(working_file, 'w') as f:
            f.write('')
        
    # open file wait for execution
    # add '#' to those tat will be excluded
    spawn_program(working_file,
                     path = r'C:\WINDOWS\system32\notepad.exe',
                     command = 'notepad', wait_mode = os.P_WAIT)

    return read_data_fr_file(working_file)


