# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 09:32:47 2015

@author: ppxdep


jobid.py optional_comment_for_this_job

returns JOBID

TODO:
    - implement argparser thing for commandline arguments
    - possible options
        o JOBID only
        o JOBID.hostname
        o print details of an old job
    - work out some standard way of including this in other scripts

"""

import sys
import csv
import os
import socket
from datetime import datetime

def main(argv):
    jobid(argv)
    
def jobid(argv):
    jobid_log = os.path.dirname(os.path.realpath(sys.argv[0])) + "\jobid.log"
    hostname = socket.gethostname()
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    # Open file in binary mode for reading and writing
    # Binary mode makes sure the csv writes do not add
    # in loads of empty lines.
    # Read the lines into an list, rows
    with open(jobid_log,"ab+") as f:
        reader = csv.reader(f)
        rows = list(reader)
        
    # If the file is empty, then we have just created it
    # In which case add a line for column headings
    if os.stat(jobid_log).st_size == 0:
        with open(jobid_log,"ab+") as f:
            writer = csv.writer(f)
            writer.writerow(["JOBID", "time","comment"])

    # Increment to get next JOBID
    try:
        oldid = rows[-1][0] 
        (number, hostname) = oldid.split('.')        
        JOBID = int(number) + 1
    except:
        JOBID = 0
    
    # Look for a comment provided as an argument
    try:
        comment = sys.argv[1]
    except:
        comment = "-"
    # Including the hostname in the JOBID makes it easier 
    # to find files later e.g. search for '1234.hostname',
    # rather than '1234', which there may well be many of
    JOBID = str(JOBID) + '.' + hostname    
    
    with open(jobid_log,"ab+") as f:
        writer = csv.writer(f)
        writer.writerow([JOBID, time_stamp, comment])
    
    
    print JOBID
    return JOBID

if __name__ == "__main__":
    main(sys.argv)
