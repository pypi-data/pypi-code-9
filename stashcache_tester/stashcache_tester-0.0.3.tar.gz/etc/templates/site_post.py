#!//usr/bin/env python

import sys
import glob
import re
import json
import os


class Test:
    def __init__(self):
        self.starttime = 0
        self.endtime = 0
        self.success = False
    


def main():
    """
    Process all of the output from the sites
    """
    
    site = sys.argv[1]
    
    # First, get a list of all the files to read 
    filelist = glob.glob(os.path.join(site, "output.*"))
    
    # Read through the files, keeping starting and ending dates
    # for each test
    start_re = re.compile("^starttime=([\d]+)$")
    end_re = re.compile("^endtime=([\d]+)$")
    result_re = re.compile("^result=([\w]+)$")
    
    tests = []
    
    for file in filelist:
        new_test = Test()
        f = open(file, 'r')
        for line in f:
            if start_re.search(line):
                match = start_re.search(line)
                new_test.starttime = match.group(1)
            elif end_re.search(line):
                match = end_re.search(line)
                new_test.endtime = match.group(1)
            elif result_re.search(line):
                match = result_re.search(line)
                if match.group(1) == "unsuccessful":
                    new_test.success = False
                elif match.group(1) == "successful":
                    new_test.success = True
                else:
                    new_test.success = None
        tests.append(new_test.__dict__)
    
    outputfile = "postprocess.%s.json" % site
    with open(outputfile, 'w') as f:
        f.write(json.dumps(tests))
    
    return 0
                
        

if __name__ == "__main__":
    sys.exit(main())
