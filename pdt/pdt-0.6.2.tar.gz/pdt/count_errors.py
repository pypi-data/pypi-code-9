#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os, sys, glob


def count_errors(error_dir):
    no_primary_taxonomy = 0
    phone_number = 0
    state_code = 0
    country_code = 0
   
    globber = os.path.join(error_dir, '*.json')
    #print glob.glob(globber)
    for f in glob.glob(globber):
        fh = open(f,"r")
        fs = fh.read()
        if fs.__contains__("taxonomy code must be marked as primary"):
            no_primary_taxonomy += 1
        if fs.__contains__("telephone"):
            phone_number += 1
        if fs.__contains__("state"):
            state_code += 1
        if fs.__contains__("country_code"):
            country_code += 1
        fh.close()
    
    print "No Taxonomy Code", no_primary_taxonomy
    print "Telephone malformed", phone_number
    print "State code error", state_code
    print "Country code error", country_code
if __name__ == "__main__":
  

    error_dir = sys.argv[1]
    count_errors(error_dir)
    