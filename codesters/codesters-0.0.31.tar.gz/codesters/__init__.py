from environment import *
from shapes import *
from sprite import *
from manager import *
import sys, subprocess

if sys.argv[0]:
    function_call = "codesters " + sys.argv[0]
    print function_call
    subprocess.call(function_call)
