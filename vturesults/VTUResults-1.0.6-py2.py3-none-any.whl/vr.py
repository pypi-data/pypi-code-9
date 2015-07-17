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
    
    subjects = []
    s_data = []
    marks = []
    marks_variables = []
    variable = []
    valid = []

    self.usn = usn
    if len(usn) == 10:
      soup = get_result(usn)
      validness = soup.find_all('td', {'width': '513'})
      for i in validness:
        valid.append(i.text)
      valid = valid[0].split()
      
      if 'not' in valid:
        print "Invalid USN"
        print "*******************************************************************************************************"  
      else:
        # finding all the subjects
        subject = soup.find_all('i')
        for i in subject:
            subjects.append(i.text)
        # finding the student data
        student_data = soup.find_all('b')
        for i in student_data:
            s_data.append(i.text)
        # finding the student's marks
        mark = soup.find_all('td', {'align' : 'center'})
        for i in mark:
            marks.append(i.text)
        
        external = marks[4::4]
        internal = marks[5::4]
        total = marks[6::4]
        status = marks[7::4]    
        
        variables = soup.find_all('td')
        for i in variables:
            marks_variables.append(i.text)
        print "*******************************************************************************************************"    
        print "ta-da!\n"    
        print "Name : "+s_data[2]
        print s_data[3] + " "+ s_data[4]+"\n"

        print "{0:47s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
        for i,j,k,l,m in zip(subjects, external, internal, total, status):
            print '{0:50s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
        
        print "\n"    
        total_marks = int(marks_variables[97])
        sem = int(s_data[4])
        print "Total Marks : ", total_marks
        
        if sem == 8:
          print "Average : ",round(float(total_marks * 100)/750, 2)
        elif sem == 1 or sem == 2:
          print "Average : ",round(float(total_marks * 100)/775, 2)
        else:
          print "Average : ",round(float(total_marks * 100)/900, 2)

        res =  s_data[5].split()[1:] 
        print 'Result : '+' '.join(res)
        print "Congratulations!"
        print "Bye "+s_data[2]+", see you later!"
        print "*******************************************************************************************************"
  
    else:
      print "Invalid USN"
      print "*******************************************************************************************************"


'''
  def get_usn(self, usn):
    self.usn = usn
    if len(usn) == 10:
      html = get_result(usn)
      valid = html.xpath('//td[@width="513"]/text()')
      if 'not' in valid:
        print "Invalid USN"
      else:
        subjects = html.xpath('//i/text()')
        marks = html.xpath('//td[@width=60][@align="center"]/text()')
        student_details = html.xpath('//b/text()')
        t_marks = html.xpath('//td/text()')
        if 'not' in t_marks[35]:
          print "Invalid USN"
        else:
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

      '''