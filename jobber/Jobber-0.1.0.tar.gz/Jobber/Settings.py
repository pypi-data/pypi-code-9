'''
Contains paths and settings
'''
import os

#if "JOBBER_CONFIG" not in os.environ:
#    sys.stderr.write("Could not find configuration. Please specify full path of configuration in environment variable JOBBER_CONFIG\n")
#    sys.exit(1)

drmaaMaxNrOfJobs = 1000
execfile(os.path.join(os.path.expanduser("~"), ".jobber/config.py"))
