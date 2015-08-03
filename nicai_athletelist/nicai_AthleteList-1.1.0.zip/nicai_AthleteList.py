class AthleteList(list):
    def __init__(self,a_name,a_dob=None,a_times=[]):
        list.__init__([])
        self.name = a_name
        self.dob=a_dob
        self.extend(a_times)

    def top3(self):
        return sorted(set([sanitize(t) for t in self]))[0:3]

"""    def add_time(self,time_value):
        self.times.append(time_value)
    def add_times(self,time_list):
        self.times.extend(time_list)"""

def sanitize(time_string):
    if '-' in time_string:
        (mins,secs) = time_string.split('-')
    elif ':' in time_string:
        (mins,secs) = time_string.split(':')
    else:
        return(time_string)
    return(mins+'.'+secs)

def open_file(path):
    try:
        with open(path) as tmpfile:
            tmpdata = tmpfile.readline()
            tmpl=tmpdata.strip().split(',')
            return (AthleteList(tmpl.pop(0),tmpl.pop(0),tmpl))
    except IOError as err:
        print("File Error:"+str(err))
        return(None)

'''james=open_file('james2.txt')
julie=open_file('julie2.txt')
mikey=open_file('mikey2.txt')
sarah=open_file('sarah2.txt')
print(james.name+"'s fastest times are:"+str(james.top3()))
print(julie.name+"'s fastest times are:"+str(julie.top3()))
print(mikey.name+"'s fastest times are:"+str(mikey.top3()))
print(sarah.name+"'s fastest times are:"+str(sarah.top3()))'''


