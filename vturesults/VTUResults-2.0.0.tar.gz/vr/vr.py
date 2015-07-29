#!/usr/bin/env python

"""
VTU Results Python Package
@author Mahesh Kumar K
@email maheshk2194@gmail.com
"""

from constants import BASE_URL
from utils import get_result, get_entire_result

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
        print "-------------------------------------------------"  
      
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
        
        external = marks[4:36:4]
        internal = marks[5:36:4]
        total = marks[6:36:4]
        status = marks[7:36:4]    
        
        variables = soup.find_all('td')
        for i in variables:
            marks_variables.append(i.text)
        
        try:
          
          sem = int(s_data[4])
          #text.append("Total Marks : "+marks_variables[97])
          
          if sem == 8:
            external = marks[4:28:4]
            internal = marks[5:28:4]
            total = marks[6:28:4]
            status = marks[7:28:4]    
            
            variables = soup.find_all('td')
            for i in variables:
                marks_variables.append(i.text)
            print "-------------------------------------------------"    
            print "ta-da!\n"    
            print "Name : "+s_data[2]
            text.append("Name : "+s_data[2])
            print s_data[3] + " "+ s_data[4]+"\n"
            text.append(s_data[3] + " "+ s_data[4])
            print "{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
            text.append("{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
            for i,j,k,l,m in zip(subjects, external, internal, total, status):
                text.append('{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
                print '{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
            
            print "\n"    
            #total_marks = int(marks_variables[97])
            total_m = 0
            for i in range(len(total)):
              total_m = total_m+int(str(total[i].encode('ascii', 'ignore')))
            #print"Total Marks caluculated using for loop is :",total_m
            print "Total Marks : ", total_m
            text.append("Total Marks : "+str(total_m))
            text.append("Average : "+str(round(float(total_m * 100)/750, 2)))
            print "Average : "+str(round(float(total_m * 100)/750, 2))
          
          elif sem == 1 or sem == 2:
            external = marks[4:36:4]
            internal = marks[5:36:4]
            total = marks[6:36:4]
            status = marks[7:36:4]    
            
            variables = soup.find_all('td')
            for i in variables:
                marks_variables.append(i.text)
            
            print "-------------------------------------------------"    
            print "ta-da!\n"    
            print "Name : "+s_data[2]
            text.append("Name : "+s_data[2])
            print s_data[3] + " "+ s_data[4]+"\n"
            text.append(s_data[3] + " "+ s_data[4])
            print "{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
            text.append("{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
            
            for i,j,k,l,m in zip(subjects, external, internal, total, status):
                text.append('{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
                print '{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
            print "\n"

            #total_marks = int(marks_variables[97])
            total_m = 0
            for i in range(len(total)-1):
              total_m = total_m+int(str(total[i].encode('ascii', 'ignore')))
            #print"Total Marks caluculated using for loop is :",sum
            print "Total Marks : ", total_m
            text.append("Total Marks : "+str(total_m))
            text.append("Average : "+str(round(float(total_m * 100)/775, 2)))
            print "Average : ",round(float(total_m * 100)/775, 2)
          
          else:
            external = marks[4:36:4]
            internal = marks[5:36:4]
            total = marks[6:36:4]
            status = marks[7:36:4]    
            
            variables = soup.find_all('td')
            for i in variables:
                marks_variables.append(i.text)
            
            print "-------------------------------------------------"    
            print "ta-da!\n"    
            print "Name : "+s_data[2]
            text.append("Name : "+s_data[2])
            print s_data[3] + " "+ s_data[4]+"\n"
            text.append(s_data[3] + " "+ s_data[4])
            print "{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
            text.append("{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
            
            for i,j,k,l,m in zip(subjects, external, internal, total, status):
                text.append('{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
                print '{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
            
            #total_marks = int(marks_variables[97])
            print "\n"
            total_m = 0
            for i in range(len(total)):
              total_m = total_m+int(str(total[i].encode('ascii', 'ignore')))
            #print"Total Marks caluculated using for loop is :",sum
            print "Total Marks : ", total_m
            text.append("Total Marks : "+str(total_m))
            text.append("Average : "+str(round(float(total_m * 100)/900, 2)))
            print "Average : ",round(float(total_m * 100)/900, 2)

          res =  s_data[5].split()[1:] 
          text.append('Result : '+' '.join(res))
          print 'Result : '+' '.join(res)
          text.append("Congratulations!")
          print "Congratulations!"
          print "Bye "+s_data[2]+", see you later!"
          for i in text:
            text_file.write(i+'\n')
          print "-------------------------------------------------"

        except ValueError, IndexError:
          print "Some Error Occured"
  
    else:
      print "Invalid USN"
      print "-------------------------------------------------"


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
          print "-------------------------------------------------"  
        
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
              
          try:
            #total_marks = int(marks_variables[97])
            sem = int(s_data[4])
            #print "Total Marks : ", total_marks
            #text.append("Total Marks : "+marks_variables[97])
            
            if sem == 8:
              external = marks[4:28:4]
              internal = marks[5:28:4]
              total = marks[6:28:4]
              status = marks[7:28:4]    
                
              variables = soup.find_all('td')
              for i in variables:
                  marks_variables.append(i.text)
              
              print "-------------------------------------------------"    
              print "ta-da!\n"    
              print "Name : "+s_data[2]
              text.append("Name : "+s_data[2])
              print s_data[3] + " "+ s_data[4]+"\n"
              text.append(s_data[3] + " "+ s_data[4])
              print "{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
              text.append("{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
              
              for i,j,k,l,m in zip(subjects, external, internal, total, status):
                  text.append('{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
                  print '{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
              
              print "\n"
              total_m = 0
              for i in range(len(total)):
                total_m = total_m+int(str(total[i].encode('ascii', 'ignore')))
              text.append("Total Marks : "+str(total_m))
              text.append("Average : "+str(round(float(total_m * 100)/750, 2)))
              print "Average : "+str(round(float(total_m * 100)/750, 2))
            
            elif sem == 1 or sem == 2:
              external = marks[4:36:4]
              internal = marks[5:36:4]
              total = marks[6:36:4]
              status = marks[7:36:4]    
                
              variables = soup.find_all('td')
              for i in variables:
                  marks_variables.append(i.text)
              print "-------------------------------------------------"    
              print "ta-da!\n"    
              print "Name : "+s_data[2]
              text.append("Name : "+s_data[2])
              print s_data[3] + " "+ s_data[4]+"\n"
              text.append(s_data[3] + " "+ s_data[4])
              print "{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
              text.append("{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
              
              for i,j,k,l,m in zip(subjects, external, internal, total, status):
                  text.append('{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
                  print '{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
              
              print "\n"
              total_m = 0
              for i in range(len(total)-1):
                total_m = total_m+int(str(total[i].encode('ascii', 'ignore')))
              text.append("Total Marks : "+str(total_m))
              text.append("Average : "+str(round(float(total_m * 100)/775, 2)))
              print "Average : ",round(float(total_m * 100)/775, 2)
            
            else:
              external = marks[4:28:]
              internal = marks[5:28:4]
              total = marks[6:28:4]
              status = marks[7:28:4]    
                
              variables = soup.find_all('td')
              for i in variables:
                  marks_variables.append(i.text)

              print "-------------------------------------------------"    
              print "ta-da!\n"    
              print "Name : "+s_data[2]
              text.append("Name : "+s_data[2])
              print s_data[3] + " "+ s_data[4]+"\n"
              text.append(s_data[3] + " "+ s_data[4])
              print "{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
              text.append("{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
              
              for i,j,k,l,m in zip(subjects, external, internal, total, status):
                  text.append('{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
                  print '{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
              
              print "\n"
              total_m = 0
              
              for i in range(len(total)):
                total_m = total_m+int(str(total[i].encode('ascii', 'ignore')))
              text.append("Total Marks : "+str(total_m))  
              text.append("Average : "+str(round(float(total_m * 100)/900, 2)))
              print "Average : ",round(float(total_m * 100)/900, 2)

            res =  s_data[5].split()[1:] 
            text.append('Result : '+' '.join(res))
            print 'Result : '+' '.join(res)
            text.append("Congratulations!")
            print "Congratulations!"
            print "Bye "+s_data[2]+", see you later!"
            for i in text:
              text_file.write(i+'\n')
            text_file.write('---------------------\n\n')
            print "-------------------------------------------------"

          except ValueError, IndexError:
            print "Some Error Occured"
    
      else:
        print "Invalid USN"
        print "-------------------------------------------------"


  # method to fetch entire results of a department
  # For every result that is fetched, it will be written to 'result.txt' 
  def get_entire_result(self):
    
    text_file = open('result_class.txt', 'w')
    rank_file = open('rank_list.txt', 'w')
    analysis_file = open('analysis_file.txt', 'w')
    final_names = []
    final_marks = []
    flag = 0
    final_average = []
    subject1 = []
    subject2 = []
    subject3 = []
    subject4 = []
    subject5 = []
    subject6 = []
    subject7 = []
    subject8 = []
    analysis = []
    
    print "-------------------------------------------------\n"
    print "Enter the USN format data as shown below \n"
    print "USN Format - 1XX11XX010"
    print "---------------- +-----------------+--------------+---------------+----------------"
    print "|    1/2/3/4     |        XX       |  11/12/13/14 |  is/cs/ec/ee  |      XXX      |"
    print "---------------- +-----------------+--------------+---------------+----------------"
    print "| (initial_code) |  (college_code) |  (year_code) | (branch_code) | (roll_number) |"
    print "-----------------+-----------------+--------------+---------------+----------------"
    
    try:
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
        total_subjects = []
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
            #print "-------------------------------------------------"  
          #else:
          if 'not' not in valid:
            # finding all the subjects
            # finding the student data
            student_data = soup.find_all('b')
            for i in student_data:
                s_data.append(i.text)
            # finding the student's marks
            mark = soup.find_all('td', {'align' : 'center'})
            for i in mark:
                marks.append(i.text)
            
            #print "\n"    
            try:
              #total_marks = int(marks_variables[97])
              sem = int(s_data[4])
              final_names.append(s_data[2])
              
              #print "Total Marks : ", total_marks
              #text.append("Total Marks : "+marks_variables[97])
              
              if sem == 8:
                subject = soup.find_all('i')
                for i in subject:
                    subjects.append(i.text)
                    if i.text in total_subjects:
                      pass
                    else:
                      total_subjects.append(i.text)
                for i in list(set(total_subjects) - set(subjects)):
                  total_subjects.append(i)
                #print "\n"+str(subjects)      
                #print "\n"+str(total_subjects)
                external = marks[4:28:4]
                internal = marks[5:28:4]
                total = marks[6:28:4]
                status = marks[7:28:4]
                #print status
                
                subject1.append(status[0])
                subject2.append(status[1])
                subject3.append(status[2])
                subject4.append(status[3])
                subject5.append(status[4])
                subject6.append(status[5])
                #subject7.append(status[6])
                #subject8.append(status[7])
                
                '''
                subject7_pass = subject1.count('P')
                subject7_fail = subject1.count('F')
                subject7_absent = subject1.count('A')
                analysis.append(subjects[6]+'\n'+'Pass : '+subject7_pass+'\n'+'Fail : '+subject7_fail+'\n'+'Absent : '+subject7_absent+'\n\n')

                subject8_pass = subject1.count('P')
                subject8_fail = subject1.count('F')
                subject8_absent = subject1.count('A')
                analysis.append(subjects[7]+'\n'+'Pass : '+subject8_pass+'\n'+'Fail : '+subject8_fail+'\n'+'Absent : '+subject8_absent+'\n\n')
                '''

                variables = soup.find_all('td')
                for i in variables:
                    marks_variables.append(i.text)
                #print "-------------------------------------------------"    
                #print "ta-da!\n"    
                #print "Name : "+s_data[2]
                text.append("Name : "+s_data[2])
                #print s_data[3] + " "+ s_data[4]+"\n"
                text.append(s_data[3] + " "+ s_data[4])
                #print "{0:47s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
                text.append("{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
                
                for i,j,k,l,m in zip(subjects, external, internal, total, status):
                    text.append('{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l, m))
                    #print '{0:50s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
                total_m = 0
                for i in range(len(total)):
                  total_m = total_m+int(str(total[i].encode('ascii', 'ignore')))
                final_marks.append(total_m)
                avg = round(float(total_m * 100)/750, 2)
                text.append("Total Marks : "+str(total_m))
                text.append("Average : "+str(avg))
                final_average.append(avg)
                #print "Average : "+str(avg)

              elif sem == 1 or sem == 2:
                external = marks[4:36:4]
                internal = marks[5:36:4]
                total = marks[6:36:4]
                status = marks[7:36:4]    
                  
                variables = soup.find_all('td')
                for i in variables:
                    marks_variables.append(i.text)
                #print "-------------------------------------------------"   
                #print "ta-da!\n"    
                #print "Name : "+s_data[2]
                text.append("Name : "+s_data[2])
                #print s_data[3] + " "+ s_data[4]+"\n"
                text.append(s_data[3] + " "+ s_data[4])
                #print "{0:47s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
                text.append("{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
                
                for i,j,k,l,m in zip(subjects, external, internal, total, status):
                    text.append('{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
                    #print '{0:50s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
                total_m = 0
                for i in range(len(total)-1):
                  total_m = total_m+int(str(total[i].encode('ascii', 'ignore')))
                final_marks.append(total_m)
                avg = round(float(total_m * 100)/775, 2)
                text.append("Total Marks : "+str(total_m))
                text.append("Average : "+str(avg))
                final_average.append(avg)
                #print "Average : "+str(avg)

              else:
                external = marks[4:28:4]
                internal = marks[5:28:4]
                total = marks[6:28:4]
                status = marks[7:28:4]    
                  
                variables = soup.find_all('td')
                for i in variables:
                    marks_variables.append(i.text)
                #print "-------------------------------------------------"
                #print "ta-da!\n"    
                #print "Name : "+s_data[2]
                text.append("Name : "+s_data[2])
                #print s_data[3] + " "+ s_data[4]+"\n"
                text.append(s_data[3] + " "+ s_data[4])
                #print "{0:47s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status")
                text.append("{0:57s} {1:10s} {2:12s} {3:12s} {4:30s}".format("Subjects", "External", "Internal", "Total", "Status"))
                
                for i,j,k,l,m in zip(subjects, external, internal, total, status):
                    text.append('{0:60s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m))
                    #print '{0:50s} {1:10s} {2:11s} {3:12s} {4:13s}'.format(i, j, k, l,m)
                total_m = 0
                
                for i in range(len(total)):
                  total_m = total_m+int(str(total[i].encode('ascii', 'ignore')))
                final_marks.append(total_m)
                avg = round(float(total_m * 100)/900, 2)
                text.append("Total Marks : "+str(total_m))
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
              print "-------------------------------------------------"

            except IndexError:
              continue
            except ValueError:
              continue
            except KeyboardInterrupt:
              print "Keyboard Interrupt"
      
        else:
            continue
          #print "-------------------------------------------------"

    except ValueError:
      print "\nSome Error Occured"
    except KeyboardInterrupt:
      print "\n Keyboard Interrupt" 
    except IndexError:
      print "\n Some Error Occurred"  
    except AttributeError:
      print "\n Some Error Occurred"

    try:
      sorted_avg = sorted(final_average, reverse=True)
      final_result = zip(final_names, final_marks)
      rank_list = sorted(final_result, key=lambda(x,y):(-y,x))
      topper, topper_marks = map(list, zip(*rank_list)) 
      
      for x,y,z in zip(topper, topper_marks, sorted_avg):
        flag += 1
        rank_file.write(str('%03d' %flag)+'. '+'{0:50s}'.format(x)+str(y)+'\t'+str(round(z, 2))+'\n')
      '''
      subject1_pass = subject1.count('P')
      subject1_fail = subject1.count('F')
      subject1_absent = subject1.count('A')
      analysis.append(subjects[0]+'\n'+'Pass : '+str(subject1_pass)+'\n'+'Fail : '+str(subject1_fail)+'\n'+'Absent : '+str(subject1_absent)+'\n\n')

      subject2_pass = subject1.count('P')
      subject2_fail = subject1.count('F')
      subject2_absent = subject1.count('A')
      analysis.append(subjects[1]+'\n'+'Pass : '+str(subject2_pass)+'\n'+'Fail : '+str(subject2_fail)+'\n'+'Absent : '+str(subject2_absent)+'\n\n')

      subject3_pass = subject1.count('P')
      subject3_fail = subject1.count('F')
      subject3_absent = subject1.count('A')
      analysis.append(subjects[2]+'\n'+'Pass : '+str(subject3_pass)+'\n'+'Fail : '+str(subject3_fail)+'\n'+'Absent : '+str(subject3_absent)+'\n\n')

      subject4_pass = subject1.count('P')
      subject4_fail = subject1.count('F')
      subject4_absent = subject1.count('A')
      analysis.append(subjects[3]+'\n'+'Pass : '+str(subject4_pass)+'\n'+'Fail : '+str(subject4_fail)+'\n'+'Absent : '+str(subject4_absent)+'\n\n')

      subject5_pass = subject1.count('P')
      subject5_fail = subject1.count('F')
      subject5_absent = subject1.count('A')
      analysis.append(subjects[4]+'\n'+'Pass : '+str(subject5_pass)+'\n'+'Fail : '+str(subject5_fail)+'\n'+'Absent : '+str(subject5_absent)+'\n\n')

      subject6_pass = subject1.count('P')
      subject6_fail = subject1.count('F')
      subject6_absent = subject1.count('A')
      analysis.append(subjects[5]+'\n'+'Pass : '+str(subject6_pass)+'\n'+'Fail : '+str(subject6_fail)+'\n'+'Absent : '+str(subject6_absent)+'\n\n')
      #print total_subjects
      #for i in subj:
        #analysis_file.write(format('{0:50s}'.format(i)+'\n'))
        #analysis_file.write(format('{0:50s}'.format(str(i))+'\n'))
    '''   
    except ValueError:
      print "\nSome Error Occured"
    except KeyboardInterrupt:
      print "\n Keyboard Interrupt" 
    except IndexError:
      print "\n Some Error Occurred"  
    print "\nDetailed Result and Rank List files have been generated.\nThe End!"    
    #analysis.append(str(total_subjects))
    text_file.close()
    rank_file.close()
    #analysis_file.close()
    