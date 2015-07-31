import os
os.chdir('/home/satish/Dropbox/Python/Learn/satish_inampudi/')
try:
    data_file = open('sketch.txt')
    for each_line in data_file:
        try:
            (role,line2read) = each_line.split(': ',1)
            print(role,end='')
            print(' said: ',end='')
            print(line2read,end='')
        except ValueError:
            pass
    data_file.seek(0) #Seek(0) takes the cursor back to starting of file
    data_file.close()    
except IOError:
    print('Data file is missing')
