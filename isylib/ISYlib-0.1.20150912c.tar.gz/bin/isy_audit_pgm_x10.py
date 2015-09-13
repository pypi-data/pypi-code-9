#!/usr/bin/env python

__author__ = "Peter Shipley"
#
#  quick hack to check what X10 device are in use by which programs
#
#  then report :
#       program name and X10 ids used
#
#       summary list of all X10 ids
#
# TODO : add options
#

# print program's full path include parent folder
opt_fullpath = True


import xml.etree.ElementTree as ET

import ISY
   
def list_prog_x10(isy) :

    # a set for all referanced cars
    x10_used_all = set()

    x10_use_count = dict()

    if opt_fullpath :
        name_width = 45
    else :
        name_width = 24

    # iterate though all programs and program folders
    for p in isy.prog_iter():

        x10_used = [ ]

        # skip root folder.
        if p.id == '0001' :
            continue

        # get D2D src for program
        src_xml = isy.prog_get_src(p.id)

        # print "src_xml", src_xml

        # parse the D2D code ( XML format )
        src_info = ET.fromstring(src_xml)

        # find all the referances to program x10
        # and store them in an array
        for v in src_info.iter("x10") :
            try :
                hc = v.find('hc').text
                uc = v.find('uc')
                if uc is not None :
                    uc = uc.text
                else :
                    uc = ""
                xid = hc + ":" + uc
                x10_used.append(xid)
                x10_use_count[xid] = x10_use_count.get(xid, 0) + 1
            except :
                print "Error : ", src_xml
                raise

        # print "iter x10 : P ", p, "x10_used", x10_used

        for v in src_info.iter("device") :
            try :
                no = v.find('node')
                if no is None :
                    continue
                if hasattr(no, 'text') and no.text is not None : 
                    no_addr = no.text.split()
                else :
                    continue
                if no_addr[0] == "FF" :
                    xid = "{:s}:{:d}".format(
                            ( unichr(64 +  int(no_addr[1], 16))),
                            int(no_addr[2], 16)
                        )

                    x10_used.append(xid)
                    x10_use_count[xid] = x10_use_count.get(xid, 0) + 1
            except :
                print "Error : ", src_xml
                raise

        # print "iter node : PID ", p, "x10_used", x10_used
        # convert the array into a set
        x10_used_set = set(x10_used)


        x10_list = sorted(x10_used_set)

        # add this set to total used set
        x10_used_all.update(x10_used_set)

        # referance program by name or full path
        if p.parentId == '0001' or opt_fullpath == False  :
            pname = p.name
        else :
            pname = p.path
            

        # if program has x10, print name and list x10 obj it contains.
        if len(x10_list) > 0 :
            print "{:<5}{:<{namew}} {!s}".format(p.id, pname, ", ".join(x10_list), namew=name_width)



    # print all x10 that are used.
    print "\nUsed X10 Ids (", len(x10_used_all), "): ",
    print str(", ").join(sorted(x10_used_all))

if __name__ == '__main__' :

    # open connection to ISY
    # don't preload node, dont subscribe to updates
    #
    # get login / pass from from Env.
    myisy = ISY.Isy(faststart=2,eventupdates=0,parsearg=1)

    # preload programs 
    myisy.load_prog()

    list_prog_x10(myisy)

    exit(0)
