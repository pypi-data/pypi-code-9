""" Create a location on filesystem for test information.

An exam is another name for 'test', to differentiate from all the test
driven, unittest, and other nomenclature. Provides a unique filesystem
location for the exam test data, pre-populated with useful system
information.
"""

import os
import time

from wpexam.systeminfo import SystemInfo

class Exam(object):
    def __init__(self, name="default", exam_root="exam_results",
                 node_name=None):

        self.si = SystemInfo()
        self.node = node_name
        if node_name == None:
            self.node = self.si.node

        self.exam_root = exam_root

        self.exam_increment = self.find_last_exam(self.exam_root,
                                                  self.node)

        self.exam_dir = "%s/%s/%s" % (self.exam_root, self.node,
                                         self.exam_increment)

        check = os.path.exists(self.exam_dir)

        print "Creating directory for this exam: %s"  % self.exam_dir
        result = os.makedirs(self.exam_dir)
       
        # Add the system info file
        sys_filename = "%s/%s_system_info.txt" % (self.exam_dir,
                                                  self.exam_increment)
        sysfile = open(sys_filename, 'w')
        sysfile.write("Exam started on %s at local time: %s\n" %
                      (self.node, time.time())
                     )

        sysfile.write("Exam description: %s\n" % name)
        sysfile.write("System summary: %s\n" % self.si.summary)
        sysfile.close()

    def find_last_exam(self, exam_root, node):
        # Walk the directory, find the largest number, add one
        if not os.path.exists(exam_root):
            print "Can't find %s (exam root), start at 1" % exam_root
            return "1"

        exam_top = "%s/%s" % (exam_root, node)
        if not os.path.exists(exam_top):
            print "Can't find %s (exam top), start at 1" % exam_top
            return "1"

        # Sort directory names in numerical order
        dirnames = os.listdir(exam_top)
        dirnames = [int(x) for x in dirnames]
        dirnames.sort()


        last_num = int(dirnames[-1])
        last_num += 1
        return last_num
        

