import math 
import numpy as np
import scipy as sp
import scipy.stats
import os
import sys
import FileDialog
from tkFileDialog import askopenfilename

import matplotlib 
matplotlib.use('TkAgg') 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg 
from matplotlib.figure import Figure 

if sys.version_info[0] < 3:
	import Tkinter as Tkinter
else:
	import tkinter as Tkinter

global hist_data
root = Tkinter.Tk() 
root.wm_title("Histogram Browser") 

fig = Figure(figsize=(5,4), dpi=100) 
ax = fig.add_subplot(111) 

canvas = FigureCanvasTkAgg(fig, master=root) 
canvas.show() 
canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1) 

toolbar = NavigationToolbar2TkAgg( canvas, root ) 
toolbar.update() 
canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1) 

histogram_bins = 1
real_data = []

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

def browse():
	global a, f, histogram_bins, hist_data, photons
	real_data = []
	ax.clear()
	fname = askopenfilename()
	photons = loadRawData(fname, 20e4)
	string.set(fname)
	hist_data = threshold_algorithm_1(0, photons)
	ax.hist(hist_data, histogram_bins)
	fig.canvas.draw()

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
'''
helper method to return only the x-coordinates (time) of the peaks
'''

def threshold_algorithm(threshold_value, data):
    arrival_times = []
    maxtab, mintab = peakdet(data,threshold_value)
    
    for integer in range(0, len(maxtab)):
        arrival_times.append(maxtab[integer][0])
    return arrival_times
'''
helper method to return only the y-coordinates (peak values) of the peaks
'''
def threshold_algorithm_1(threshold_value, data):
    peak_values = []
    maxtab, mintab = peakdet(data,threshold_value)
    
    for integer in range(0, len(maxtab)):
        peak_values.append(maxtab[integer][1])
    return peak_values

def change_bins():
	global histogram_bins

	histogram_bins += 5
	ax.clear()
	ax.hist(hist_data, histogram_bins)

	ax.set_ylim(0, 1000)

	fig.canvas.draw()
def decrement():
    global histogram_bins

    histogram -= 5
    ax.clear()
    ax.hist(hist_data, histogram_bins)

    ax.set_ylim(0, 1000)

    fig.canvas.draw()
def optimal_bin():
    global histogram_bins, photons
    ax.clear()
    temp_data = []
    bin_count = 1
    while 0 not in temp_data:
        temp_data, x = np.histogram(photons, bins = bin_count)
        bin_count += 1
    hist, bin_edges = np.histogram(photons, bins = bin_count)
    hist, bin_edges = np.histogram(photons, bins = bin_count-1)
    ax.bar(bin_edges[:-1], hist)
    ax.set_xlim(min(bin_edges), max(bin_edges))
    fig.canvas.draw()

string = Tkinter.StringVar()
lab = Tkinter.Label(root, textvariable = string, fg = 'white', bg = 'black', font = "Verdana 10 bold")
lab.pack()

button = Tkinter.Button(master=root, text='Input File', command=browse, font = "Helvetica 16 bold") 
button.pack(fill='x', side=Tkinter.TOP)


button1 = Tkinter.Button(master=root, text = "Increment", command=change_bins, fg = 'red', font = "Helvetica 16 bold")
button1.pack( fill = 'both')

button2 = Tkinter.Button(master = root, text = "Decrement", command = decrement, fg = 'red', font = "Helvetica 16 bold")
button2.pack(fill = 'both')

button3 = Tkinter.Button(master = root, text = "Find Optimal Bin Size", command = optimal_bin, fg = 'black', font = "Helvetica 16 bold")
button3.pack(fill = 'both')

root.geometry('{}x{}'.format(800, 700))
Tkinter.mainloop() 