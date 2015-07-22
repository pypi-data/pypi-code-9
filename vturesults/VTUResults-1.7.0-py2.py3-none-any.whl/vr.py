#!/usr/bin/env python

"""
VTU Results Python Package
@author Mahesh Kumar K
@email maheshk2194@gmail.com
"""

from constants import BASE_URL
from utils import get_result, get_entire_result
import sys

class VR(object):

  def __init__(self):
    pass

  # Method to fetch single USN Result
  # For every result that is fetched, it will be written to 'result.txt'  
  def get_usn(self, usn):
    
    subjects = []
    s_data = []
    marks = []
    marks_variables = []
    variable = []
    valid = []
    text = []
    text_file = open('result.txt', 'w')
    self.usn = usn
    if len(usn) == 10:
      # function to fetch the html format of the request usn's result
      soup = get_result(usn)
      validness = soup.find_all('td', {'width': '513'})
      for i in validness:
        valid.append(i.text)
      valid = valid[0].split()
      
      if 'not' in valid:
        print "Invalid USN"
        print "---------------------------------------------------------------------------------------------------"  
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
        print "---------------------------------------------------------------------------------------------------"    
        print "ta-da!\n"    
        print "Name : "+s_data[2]
        text.append("Name : "+s_data[2])
        print s_data[3] + " "+ s_data[4]+"\n"
        text.append(s_data[3] + " "+ s_data[4])
        print "{0:47s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
        text.append("{0:47s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
        for i,j,k,l,m in zip(subjects, external, internal, total, status):
            text.append('{0:50s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
            print '{0:50s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
        
        print "\n"    
        try:
          total_marks = int(marks_variables[97])
          sem = int(s_data[4])
          print "Total Marks : ", total_marks
          #text.append("Total Marks : "+marks_variables[97])
          
          if sem == 8:
            text.append("Average : "+str(round(float(total_marks * 100)/750, 2)))
            print "Average : "+str(round(float(total_marks * 100)/750, 2))
          elif sem == 1 or sem == 2:
            text.append("Average : "+str(round(float(total_marks * 100)/775, 2)))
            print "Average : ",round(float(total_marks * 100)/775, 2)
          else:
            text.append("Average : "+str(round(float(total_marks * 100)/900, 2)))
            print "Average : ",round(float(total_marks * 100)/900, 2)

          res =  s_data[5].split()[1:] 
          text.append('Result : '+' '.join(res))
          print 'Result : '+' '.join(res)
          text.append("Congratulations!")
          print "Congratulations!"
          print "Bye "+s_data[2]+", see you later!"
          for i in text:
            text_file.write(i+'\n')
          print "---------------------------------------------------------------------------------------------------"

        except ValueError, IndexError:
          print "Some Error Occured"
  
    else:
      print "Invalid USN"
      print "---------------------------------------------------------------------------------------------------"


  # Method to fetch results for multiple USN
  # For result that is fetched, result will be written to 'results.txt'    
  def get_group_usn(self): 
    number = input("Enter the total number of USN, for which you want to get result : ")
    text_file = open('results.txt', 'w')
    for i in range(number):
      usn = raw_input("Enter {} USN : ".format(i+1))
      subjects = []
      s_data = []
      marks = []
      marks_variables = []
      variable = []
      valid = []
      text = []
      self.usn = usn
      if len(usn) == 10:
        # function to fetch the html format of the request usn's result
        soup = get_result(usn)
        validness = soup.find_all('td', {'width': '513'})
        for i in validness:
          valid.append(i.text)
        valid = valid[0].split()
        
        if 'not' in valid:
          print "Invalid USN"
          print "---------------------------------------------------------------------------------------------------"  
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
          print "---------------------------------------------------------------------------------------------------"    
          print "ta-da!\n"    
          print "Name : "+s_data[2]
          text.append("Name : "+s_data[2])
          print s_data[3] + " "+ s_data[4]+"\n"
          text.append(s_data[3] + " "+ s_data[4])
          print "{0:47s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
          text.append("{0:47s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
          for i,j,k,l,m in zip(subjects, external, internal, total, status):
              text.append('{0:50s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
              print '{0:50s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
          
          print "\n"    
          try:
            total_marks = int(marks_variables[97])
            sem = int(s_data[4])
            print "Total Marks : ", total_marks
            #text.append("Total Marks : "+marks_variables[97])
            
            if sem == 8:
              text.append("Average : "+str(round(float(total_marks * 100)/750, 2)))
              print "Average : "+str(round(float(total_marks * 100)/750, 2))
            elif sem == 1 or sem == 2:
              text.append("Average : "+str(round(float(total_marks * 100)/775, 2)))
              print "Average : ",round(float(total_marks * 100)/775, 2)
            else:
              text.append("Average : "+str(round(float(total_marks * 100)/900, 2)))
              print "Average : ",round(float(total_marks * 100)/900, 2)

            res =  s_data[5].split()[1:] 
            text.append('Result : '+' '.join(res))
            print 'Result : '+' '.join(res)
            text.append("Congratulations!")
            print "Congratulations!"
            print "Bye "+s_data[2]+", see you later!"
            for i in text:
              text_file.write(i+'\n')
            text_file.write('---------------------\n\n')
            print "---------------------------------------------------------------------------------------------------"

          except ValueError, IndexError:
            print "Some Error Occured"
    
      else:
        print "Invalid USN"
        print "---------------------------------------------------------------------------------------------------"


  # method to fetch entire results of a department
  # For every result that is fetched, it will be written to 'result.txt' 
  def get_entire_result(self):
    text_file = open('result_class.txt', 'w')
    rank_file = open('rank_list.txt', 'w')
    final_names = []
    final_marks = []
    flag = 0
    final_average = []
    print "------------------------------------------------------------------"
    print "Enter the USN format data as shown below "
    print "USN Format - 1XX11XX010"
    print "1 - Initial Code \nXX - College Code \n11 - Year Code \nXX Branch Code \n010 - Roll No\n"
    print "---------------- +-----------------+--------------+---------------+----------------"
    print "| (initial_code) |  (college_code) |  (year_code) | (branch_code) | (roll_number) |"
    print "-----------------+-----------------+--------------+---------------+----------------"
    initial_code = raw_input("Enter the first Character in your USN : ")
    college_code = raw_input("Enter your college code in the USN : ")
    year_code = raw_input("Enter your year code in the USN : ")
    branch_code = raw_input("Enter your branch code in the USN : ")
    total_strength = input("Enter the total strength of your  class or department : ")
    print "\n"
    for i in range(total_strength):
      bar_length = 60
      percent = float(i) / total_strength
      hashes = '=' * int(round(percent * bar_length))
      spaces = ' ' * (bar_length - len(hashes))
      sys.stdout.write("\rCrunching Data: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
      sys.stdout.flush()
      
      usn = initial_code+college_code+year_code+branch_code+str('%03d' %i)
      subjects = []
      s_data = []
      marks = []
      marks_variables = []
      variable = []
      valid = []
      text = []
      self.usn = usn
      if len(usn) == 10:
        # function to fetch the html format of the request usn's result
        soup = get_entire_result(usn)
        validness = soup.find_all('td', {'width': '513'})
        for i in validness:
          valid.append(i.text)
        valid = valid[0].split()
        
        #if 'not' in valid:
          #print "\nInvalid USN " 
          #print "---------------------------------------------------------------------------------------------------"  
        #else:
        if 'not' not in valid:
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
          #print "---------------------------------------------------------------------------------------------------"    
          #print "ta-da!\n"    
          #print "Name : "+s_data[2]
          text.append("Name : "+s_data[2])
          #print s_data[3] + " "+ s_data[4]+"\n"
          text.append(s_data[3] + " "+ s_data[4])
          #print "{0:47s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
          text.append("{0:47s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
          for i,j,k,l,m in zip(subjects, external, internal, total, status):
              text.append('{0:50s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
              #print '{0:50s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
          
          #print "\n"    
          try:
            total_marks = int(marks_variables[97])
            sem = int(s_data[4])
            final_names.append(s_data[2])
            final_marks.append(total_marks)
            #print "Total Marks : ", total_marks
            #text.append("Total Marks : "+marks_variables[97])
            
            if sem == 8:
              avg = round(float(total_marks * 100)/750, 2)
              text.append("Average : "+str(avg))
              final_average.append(avg)
              #print "Average : "+str(avg)
            elif sem == 1 or sem == 2:
              avg = round(float(total_marks * 100)/775, 2)
              text.append("Average : "+str(avg))
              final_average.append(avg)
              #print "Average : "+str(avg)
            else:
              avg = round(float(total_marks * 100)/900, 2)
              text.append("Average : "+str(avg))
              final_average.append(avg)
              #print "Average : "+str(avg)

            res =  s_data[5].split()[1:] 
            text.append('Result : '+' '.join(res))
            #print 'Result : '+' '.join(res)
            text.append("Congratulations!")
            #print "Congratulations!"
            #print "Bye "+s_data[2]+", see you later!"
            for i in text:
              text_file.write(i+'\n')
            #print "Total Marks List Length",len(final_marks)
            #print "Total Names List Length",len(final_names)
            #print final_marks
            #print final_names
            text_file.write('---------------------\n\n')
            #print "---------------------------------------------------------------------------------------------------"

          except ValueError, IndexError:
            continue
    
      #else:
       # print "\nInvalid USN" 
        #print "---------------------------------------------------------------------------------------------------"
    
    print "\nDetailed Result and Rank List files have been generated.\nThe End!"
    sorted_avg = sorted(final_average, reverse=True)
    final_result = zip(final_names, final_marks)
    rank_list = sorted(final_result, key=lambda(x,y):(-y,x))
    topper, topper_marks = map(list, zip(*rank_list)) 
    for x,y,z in zip(topper, topper_marks, sorted_avg):
      flag += 1
      rank_file.write(str('%03d' %flag)+'. '+'{0:50s}'.format(x)+str(y)+'\t'+str(round(z, 2))+'\n')
    text_file.close()
    rank_file.close()
    