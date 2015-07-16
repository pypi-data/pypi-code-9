#!/usr/bin/env python

"""
VTU Results Python Package
@author Mahesh Kumar K
@email maheshk2194@gmail.com
"""

from constants import BASE_URL
from utils import get_result

class VR(object):
  def __init__(self):
    pass

  def get_usn(self, usn):
    self.usn = usn
    if len(usn) == 10:
      html = get_result(usn)
      subjects = html.xpath('//i/text()')
      marks = html.xpath('//td[@width=60][@align="center"]/text()')
      student_details = html.xpath('//b/text()')
      t_marks = html.xpath('//td/text()')
      total_marks = int(t_marks[61])
      student_name = student_details[0]
      semester = int(student_details[2])
      result = student_details[3].encode('ascii','ignore')
      print "******************************************************************"
      print "Name : "+student_name
      print "Semester: ",semester
      print "Marks format is : Subject Name / Internal / External / Total"
      if  subjects:
          internal = marks[5::3]
          external = marks[4::3]
          total = marks[6::3]     
          for i,j,k,l in zip(subjects, internal, external, total):
              print i,j,k,l
          print "Total Marks = ",total_marks
          if semester == 8:
              print "Average = ",round(float(total_marks * 100)/750, 2)
          elif semester == 1 or semester == 2:
              print "Average = ",round(float(total_marks * 100)/775, 2)
          else:
              print "Average = ",round(float(total_marks * 100)/900, 2)
          print "Result = "+result[8:]
          print "complete result obtained"
          print "******************************************************************"

    else:
      return "Invalid USN"
      print "******************************************************************"