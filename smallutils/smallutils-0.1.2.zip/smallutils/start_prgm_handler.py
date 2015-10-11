"""

 Start prgram handler 
 Author: Tan Kok Hua 
 Email: Kokhua81@gmail.com

"""

import sys
import os
import subprocess

PYTHON_PATH = r'C:\Python%s'% (str(sys.version_info[0])+ str(sys.version_info[1]))
PYTHON_VER_NO = str(sys.version_info[0])+ str(sys.version_info[1])

def spawn_program(filename, path = os.path.join(PYTHON_PATH,'python'), command ='python', wait_mode = os.P_WAIT):
    """
        need to enter a single quote follow by double quote
        eg: '"c:\\data\\example.py"'
        adding args:
            eg:'"C:\\SETS Files\\Python\\Examples\\Script1_try.py" 1 2'
        if error, return one,else return 0

        Wait_mode option allow user to specify whether to wait for program to finish or continue with next commands
        Input in os.P_WAIT(0) or os.P_NOWAIT(1)       
       
    """
    
    try:
        results = os.spawnv(wait_mode, path ,[command,filename])

    finally:
        if results !=0:
            print 'Error in running program'
            return 1
    return 0


def open_program(filename,path = os.path.join(PYTHON_PATH,'python.exe'), args = [], display_off =1):
    """
        Option to select whether to display the console windows
        display_off = 1 means that the console is not displayed.

        args should in a list and contain in a str. Separate each args as each elem in a list.   
        
        NB: Will NOT wait for the ext program to finish. Will
        continue with script once launch program
    """
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags = subprocess._subprocess.STARTF_USESHOWWINDOW
    #startupinfo.wShowWindow
    total_filename = [filename,] + args
    if display_off:
        status = subprocess.Popen([path]+ total_filename,startupinfo=startupinfo)
    else:
        status = subprocess.Popen([path]+ total_filename)
    return status
    #print status
        
def run_program_multi_cycles(file,path = os.path.join(PYTHON_PATH,'python'), command ='python', sleep_time = 0.1, loop_cycles =1):
    """
        Sleep time in secs
    """
    import time
    
    for n in range(loop_cycles):
        print 'This is the  ', n + 1, '  loop out of total  ',loop_cycles
        spawn_program(file,path,command)
        print 'will sleep for  ', sleep_time, ' sec'
        time.sleep(sleep_time)

    print 'Finished'

    

