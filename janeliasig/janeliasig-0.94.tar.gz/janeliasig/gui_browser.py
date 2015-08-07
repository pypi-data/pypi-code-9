import math 
import numpy as np
import scipy as sp
from scipy import stats, signal 
import matplotlib 
matplotlib.use('TkAgg') 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg 
from matplotlib.figure import Figure 
import scipy.stats
import os
import sys
import FileDialog
from tkFileDialog import askopenfilename



if sys.version_info[0] < 3:
	import Tkinter as Tkinter
else:
	import tkinter as Tkinter
import tkMessageBox

root = Tkinter.Tk() 
root.wm_title("GUI Browser") 

fig = Figure(figsize=(5,4), dpi=100) 
ax = fig.add_subplot(111) 

canvas = FigureCanvasTkAgg(fig, master=root) 
canvas.show() 
canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1) 

toolbar = NavigationToolbar2TkAgg( canvas, root ) 
toolbar.update() 
canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1) 

plotShift = 0
#
#the window values
current_xmin = 0
current_xmax = 500
current_ymin = -5
current_ymax = 25

negative_axis = False
#
#the placeholder for where the unpacked data will go
real_data = []

def x_minimize(): 
    global  a, f, current_xmin, current_xmax, current_ymin, current_ymax
    
    
    
    
    current_xmin -= (current_xmax - current_xmin) * 0.1
    current_xmax += (current_xmax - current_xmin) * 0.1
    ax.set_xlim(current_xmin, current_xmax)
    fig.canvas.draw() 


def x_maximize():
    global  a, f, current_xmin, current_xmax, current_ymin, current_ymax
    
    
    
    current_xmin += (current_xmax - current_xmin) * 0.1
    current_xmax -= (current_xmax - current_xmin) * 0.1
    ax.set_xlim(current_xmin, current_xmax)
    fig.canvas.draw() 

def y_minimize():
    global  a, f, current_xmin, current_xmax, current_ymin, current_ymax
    current_ymin -= (current_ymax - current_ymin) * 0.1
    current_ymax += (current_ymax - current_ymin) * 0.1
    ax.set_ylim(current_ymin, current_ymax)
    fig.canvas.draw() 
def y_maximize():
    global  a, f, current_xmin, current_xmax, current_ymin, current_ymax
    current_ymin += (current_ymax - current_ymin) * 0.1
    current_ymax -= (current_ymax - current_ymin) * 0.1
    ax.set_ylim(current_ymin, current_ymax)
    fig.canvas.draw() 
def shift_right_key(event): 
    global plotShift, a, f, current_xmin, current_xmax
    
    
    
    plotShift = current_xmax - current_xmin
    current_xmin += plotShift
    current_xmax += plotShift
    ax.set_xlim(current_xmin, current_xmax)
    fig.canvas.draw() 

#Moves the x lim to the left by (plotShift = 10)
def shift_left_key(event):
    global plotShift, a, f, current_xmin, current_xmax
    
    plotShift = current_xmin- current_xmax
    current_xmin += plotShift
    current_xmax += plotShift
    ax.set_xlim(current_xmin, current_xmax)
    fig.canvas.draw()
#Algorithm converted from .mat file 

def shift_up_key(event):
    global plotShift, a, f, current_ymin, current_ymax
    
    plotShift = current_ymax - current_ymin
    current_ymin += plotShift
    current_ymax += plotShift
    ax.set_ylim(current_ymin, current_ymax)
    fig.canvas.draw()
def shift_down_key(event):
    global plotShift, a, f, current_ymin, current_ymax
    
   
    plotShift = current_ymin - current_ymax
    current_ymin  += plotShift
    current_ymax += plotShift
    ax.set_ylim(current_ymin, current_ymax)
    fig.canvas.draw()
def loadRawData(filename, num_elements = float("inf"), sourcedataformat = 'int8', target_dataformat = 'int8'):

    #dirinfo = dir(filename)
    file_size_bytes = os.path.getsize(filename)
   
    def doInt8(): 
        #bytesperelement = 1
        return 1
    def doInt16():
        #bytesperelement = 2
        return 2
    def doInt32():
        #bytesperelement = 4
        return 4
    def doInt64():
        #bytesperelement = 8
        return 8
    def error():
        print "Your input has not been recognized"
    formats = {
        'int8': doInt8(),
        'uint8': doInt8(),
        'int16': doInt16(),
        'uint16': doInt16(),
        'int32': doInt32(),
        'uint32': doInt32(),
        'int64': doInt64(),
        'uint64': doInt64()}
    
    bytes_per_element = formats.get(sourcedataformat, error)
    
    num_file_elements = math.floor(file_size_bytes / bytes_per_element)
    
    num_elements = min(num_elements, num_file_elements)
    data = np.zeros(num_elements, target_dataformat)
    
    chunk_size_bytes = 50e6
    chunk_size_elements = chunk_size_bytes / bytes_per_element
    
    fileID = open(filename, 'rb')
    
    for iter in range(1, int(math.floor(num_elements/chunk_size_elements))):
         data[chunk_size_elements*(iter-1)+1: chunk_size_elements*iter] = np.fromfile(fileID, sourcedataformat, chunk_size_elements)
    
    remaining_elements = int(num_elements%chunk_size_elements)
    data[-1 - remaining_elements+1:-1] = np.fromfile(fileID, sourcedataformat, remaining_elements - 1)
   
    return data
    fileID.close()


#invokes a file browser from Tkinter module
def browse():
    global current_xmin, current_xmax, a, f, current_ymin, current_ymax, y_photons
    real_data = []
    ax.clear()
    fname = askopenfilename()
    photons = loadRawData(fname, 5e4)
    x_photons = np.linspace(0, len(photons)* (2.0/3.0), len(photons))
    y_photons = photons


    ax.plot( y_photons, 'g')
    ax.set_xlim(current_xmin, current_xmax)
    ax.set_ylim(current_ymin, current_ymax)
    
    string.set(fname)
    #string1.set("Sampling Frequency: 1.5 Gigahertz, first " + str(current_xmax - current_xmin) + " samples")
    if fname.find("ch0") == -1:
        ax.set_title("Laser Pulses")
    else:
        ax.set_title("PMT Output")
   
    ax.set_ylabel("Analog to Digital Units")
    ax.set_xlabel("Time in nanoseconds")
    m1, m2 = peak_analyze()
    
    fig.canvas.draw()
def x_change():
    global current_xmax, current_xmin, a, f, negative_axis
    current_xmin = float(diary.get())
    current_xmax = float(diary1.get())

    #string1.set("Sampling Frequency: 1.5 Gigahertz, first " + str(current_xmax - current_xmin) + " samples")
    ax.set_xlim(current_xmin, current_xmax)

    fig.canvas.draw()

def y_change():
    global current_ymax, current_ymin, a, f, negative_axis
    current_ymin = float(diary3.get())
    current_ymax = float(diary2.get())

    #string1.set("Sampling Frequency: 1.5 Gigahertz, first " + str(current_xmax - current_xmin) + " samples")
    ax.set_ylim(current_ymin, current_ymax)

    fig.canvas.draw()

def threshold_algorithm(threshold_value, data):
    arrival_times = []
    maxtab, mintab = peakdet(data,threshold_value)
    
    for integer in range(0, len(maxtab)):
        arrival_times.append(maxtab[integer][0])
    return arrival_times
def threshold_algorithm_1(threshold_value, data):
    peak_values = []
    maxtab, mintab = peakdet(data,threshold_value)
    
    for integer in range(0, len(maxtab)):
        peak_values.append(maxtab[integer][1])
    return peak_values

def threshold_algorithm_2(threshold_value, data):
    arrival_times = []
    maxtab, mintab = peakdet(data, threshold_value)

    for integer in range(0, len(mintab)):
        arrival_times.append(mintab[integer][0])
    return arrival_times
def threshold_algorithm_3(threshold_value, data):
    peak_values = []
    maxtab, mintab = peakdet(data, threshold_value)

    for integer in range(0, len(mintab)):
        peak_values.append(mintab[integer][0])
    return peak_values
def peakdet(data_array, threshold, x_axis = None):
    maxtab = []
    mintab = []
       
    if x_axis is None:
        x_axis = np.arange(len(data_array))
    
    data_array = np.asarray(data_array)
    
    if len(data_array) != len(x_axis):
        raise ValueError('Input vectors v and x must have same length')
    
    if not np.isscalar(threshold):
        raise ValueError('Input argument delta must be a scalar')
    
    if threshold < 0:
        raise ValueError('Input argument delta must be positive')
    
    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN
    
    look_for_max = True
    
    for i in np.arange(len(data_array)):
        this = data_array[i]
        if this > mx:
            mx = this
            mxpos = x_axis[i]
        if this < mn:
            mn = this
            mnpos = x_axis[i]
        
        if look_for_max:
            if this < mx-threshold:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x_axis[i]
                look_for_max = False
        else:
            if this > mn+threshold:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x_axis[i]
                look_for_max = True
 
    return np.array(maxtab), np.array(mintab)
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    return m, m-h, m+h
def show_peaks():
    global y_photons, a, f, offshoot_value, current_xmax, current_xmin, current_ymax, current_ymin
    ax.clear()
    template_list = [ 1 , 4 , 7 ,10 ,13 ,16 ,18 ,21 ,22 ,23 ,24 ,25 ,24 ,24 ,23 ,21 ,19 ,17 ,14, 12 ,10  ,8  ,5 , 3 , 1]
    zero_convoluted_data = list(y_photons)
    zero_noised_signal =   template_list

    a = zero_convoluted_data
    v = zero_noised_signal

    correlated_data = signal.correlate(a, v, mode = 'full' )
    '''
    for n in range(0, len(correlated_data)):
        if correlated_data[n] < 0:
            correlated_data[n] = 0
    '''      
    bin_count = 1
    temp_data = []
    while 0 not in temp_data:
        temp_data, x = np.histogram(correlated_data, bins = bin_count)
        bin_count += 1
        
    hist, bin_edges = np.histogram(correlated_data, bins = bin_count)

    total_count = sum(hist)
    temp_sum = 0
    threshold_value = 0
    '''
    for i in range(0, len(hist)):
        temp_sum += hist[i]
        
        if temp_sum >= total_count * 0.05 and bin_edges[i] > 0:
            threshold_value = i
            break
    '''
    total_count = sum(hist)
    temp_sum = 0
    for i in range(0, len(hist)):
        temp_sum += hist[i]
        if temp_sum >= total_count * 0.95 and bin_edges[i] > 0:
            offshoot_value = i
            break     
              
    threshold_value = 0
    offshoot_value = bin_edges[offshoot_value]

    temp_peak_times = threshold_algorithm(threshold_value,correlated_data)
    temp_peak_values = threshold_algorithm_1(threshold_value, correlated_data)
    temp_min_times = threshold_algorithm_2(threshold_value, correlated_data)
    temp_min_values = threshold_algorithm_3(threshold_value, correlated_data)
    min_values = []
    min_times = []
    peak_values = []
    peak_times = []
    temp_reached_peakhigh = False
    reached_peakhigh = False
    #print temp_peak_times[0:200], temp_peak_values[0:200]
    #print "__________________________________________"
    '''
    for c in range(0, len(temp_peak_values)):
        if reached_peakhigh:
            if temp_peak_times[c] - temp_peak_times[c-1] < 50: 
                reached_peakhigh = False
            else:
                if temp_peak_values[c] < offshoot_value:
                    peak_values.append(temp_peak_values[c])
                    peak_times.append(temp_peak_times[c])
                    reached_peakhigh = False
                else:
                    reached_peakhigh = True
            continue
        if temp_peak_values[c] < offshoot_value:
            peak_values.append(temp_peak_values[c])
            peak_times.append(temp_peak_times[c])
        if temp_peak_values[c] >= offshoot_value:
            reached_peakhigh = True
    final_peak_times = peak_times
    final_peak_values = []   
    '''

    for odi in range(0, len(temp_peak_values)):
        if temp_reached_peakhigh:
            if temp_peak_values[odi] < (offshoot_value * 0.2):
                min_values.append(abs(float(temp_peak_values[odi])/temp_peak_values[odi - 1]))
            temp_reached_peakhigh = False
        else:
            if temp_peak_values[odi] < offshoot_value:
                temp_reached_peakhigh = False
            else:
                temp_reached_peakhigh = True
                
    average_difference = np.mean(min_values)



    for c in range(0, len(temp_peak_values)):
        if reached_peakhigh:
            if abs(temp_peak_times[c]) - abs(temp_peak_times[c]) < 50: 
                if abs(temp_peak_values[c]) > (abs(temp_peak_values[c-1]) * average_difference):
                    peak_values.append(temp_peak_values[c])
                    peak_times.append(temp_peak_times[c])
                    reached_peakhigh = False
                    #print "it hit an overshoot"
                    #print temp_peak_values[c], temp_peak_times[c]
                    #print temp_min_values[c], temp_min_times[c]
                else:
                    reached_peakhigh = True
                
            else:
                if temp_peak_values[c] < offshoot_value:
                    peak_values.append(temp_peak_values[c])
                    peak_times.append(temp_peak_times[c])
                    reached_peakhigh = False
                else:
                    peak_values.append(temp_peak_values[c])
                    peak_times.append(temp_peak_times[c])
                    reached_peakhigh = True
        else:
            if temp_peak_values[c] < offshoot_value:
                peak_values.append(temp_peak_values[c])
                peak_times.append(temp_peak_times[c])
            if temp_peak_values[c] >= offshoot_value:
                reached_peakhigh = True
                peak_values.append(temp_peak_values[c])
                peak_times.append(temp_peak_times[c])
                
    final_peak_times = []
    final_peak_values = []
    for bail in range(0, len(peak_values)):
        if peak_values[bail] >= 0:
            final_peak_values.append(peak_values[bail])
            final_peak_times.append(peak_times[bail])
        
    for n in range(0, len(correlated_data)):
        if correlated_data[n] < 0:
            correlated_data[n] = 0
    ax.plot(correlated_data)
    #ax.scatter(np.array(maxtab)[:,0], np.array(maxtab)[:,1], color='green', label = "Peaks")
    #ax.scatter(np.array(mintab)[:,0], np.array(mintab)[:,1], color='red', label = "Valleys")
    ax.scatter(final_peak_times, final_peak_values)
    ax.set_title("Peak Detection on Cross Correlated Data")
    ax.set_xlabel("Time - nanoseconds")
    current_ymin = -500
    current_ymax = 5500
    ax.set_ylim(current_ymin, current_ymax)
    ax.set_xlim(current_xmin, current_xmax)
    fig.canvas.draw()
#Will not work for negatively scaled amplitudes
#Output of "nan to nan" for failures
def peak_analyze():
    global y_photons, real_data
    real_data = []
    temp_data = threshold_algorithm_1(3, y_photons)
    
    for i in range(0, len(temp_data)):
        if temp_data[i] > 2:
            real_data.append(temp_data[i])
    mean, firstm, secondm = mean_confidence_interval(real_data)
    return firstm, secondm
string = Tkinter.StringVar()
lab = Tkinter.Label(root, textvariable = string, fg = 'white', bg = 'black', font = "Verdana 10 bold")
lab.pack()

#string1 = Tkinter.StringVar()
#lab1 = Tkinter.Label(root, textvariable = string1, font = "Verdana 12 bold")
#lab1.pack()


string3 = Tkinter.StringVar()
diary = Tkinter.Entry(root, textvariable = string3, width = 20)
diary.pack(side = Tkinter.LEFT)
diary.insert(0, "Minimum X Coordinate")

string4 = Tkinter.StringVar()
diary1 = Tkinter.Entry(root, textvariable = string4, width = 20)
diary1.pack(side = Tkinter.LEFT)
diary1.insert(0, "Maximum X Coordinate")

string5 = Tkinter.StringVar()
diary2 = Tkinter.Entry(root, textvariable = string5, width = 20)
diary2.pack(side = Tkinter.RIGHT)
diary2.insert(0, "Maximum Y Coordinate")

string6 = Tkinter.StringVar()
diary3 = Tkinter.Entry(root, textvariable = string6, width = 20)
diary3.pack(side = Tkinter.RIGHT)
diary3.insert(0, "Minimum Y Coordinate")


button = Tkinter.Button(master=root, text='Input File', command=browse, font = "Helvetica 16 bold") 
button.pack(fill='x', side=Tkinter.TOP)

button2 = Tkinter.Button(master=root, text = "X (-)", command=x_minimize, fg = 'red', font = "Helvetica 16 bold")
button2.pack(side = Tkinter.LEFT, fill = 'x')
button1 = Tkinter.Button(master=root, text = "X (+)", command=x_maximize, fg = 'red', font = "Helvetica 16 bold")
button1.pack(side = Tkinter.LEFT, fill = 'x')

button6 = Tkinter.Button(master = root, text= "Y (+)", command =y_maximize, fg = 'red', font = "Heveltica 16 bold" )
button6.pack(side = Tkinter.RIGHT, fill = 'x')
button7 = Tkinter.Button(master = root, text= "Y (-)", command =y_minimize, fg = 'red', font = "Heveltica 16 bold" )
button7.pack(side = Tkinter.RIGHT, fill = 'x')

button3 = Tkinter.Button(master = root, text = 'Click to Change X-Window', command = x_change, font = "Helvetica 10 bold italic")
button3.pack(side = Tkinter.BOTTOM, fill = 'both')
button5 = Tkinter.Button(master = root, text = 'Click to Change Y-Window', command = y_change, font = "Helvetica 10 bold italic")
button5.pack(side = Tkinter.BOTTOM, fill = 'both')
button4 = Tkinter.Button(master = root, text = "Plot Detected Peaks", command = show_peaks, font = "Helvetica 10 bold italic")
button4.pack( fill = 'both')

root.bind('<Left>', shift_left_key)
root.bind('<Right>', shift_right_key)
root.bind('<Up>', shift_up_key)
root.bind('<Down>', shift_down_key)

root.geometry('{}x{}'.format(1800, 1700))
Tkinter.mainloop() 

