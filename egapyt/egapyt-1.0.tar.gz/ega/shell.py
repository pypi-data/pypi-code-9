# Shell manipulations
import subprocess
import shlex

def cmd(str):
    """
    Return a simple out, err in tuple form from a non-interactive command
    It's your job to make sure what you pass in in non-interactive, don't be a douche
    """
    out, err = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out, err
