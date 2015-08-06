'''
`filename` refers to the full directory of the .bin file. 

`num_elements` refers to the number of elements you wish to unpack from the binary file. The **default** is infinity. I **recommend** that only 50e6 elements are unpacked at a time. 

`sourcedataformat` refers to the format of the input data. The **default** is int8. 

`targetdataformat` refers to the format of the output data. The **default** is int8.

load_raw_data() is a converted file from matlab to Python. It will unpack any binary file to make it matplotlib-compatible data. The binary file is unpacked chunks at at time to decrease the chance of system crash. 
~~~~
The output is a list of all data points that you have unpacked. 
~~~~
'''
def load_raw_data(filename, num_elements = float("inf"), sourcedataformat = 'int8', target_dataformat = 'int8'):
    import os
    import math
    import numpy as np

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
    
    bytes_per_element = formats.get(sourcedataformat, 'int8')
    
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

'''
`data_array` refers to the dataset that you wish to run the detection algorithm on.

`threshold` refers to the minimum distance between a peak to a valley for the algorithm to detect it as a peak.

`x_axis` is an array of x-coordinates that go along with the `data_array`. The **default** is None. 

Will detect most peaks in any dataset. 

~~~~
The output is a tuple of two numpy arrays:(peak values and times), (valley values and times).
~~~~
***Valley refers to the minimums while peak refers to the maximums***
'''
def peakdet(data_array, threshold, x_axis = None):
    import numpy as np
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
`threshold_value`; please refer to the docstring for **peakdet()**

`data`; again, ditto above
~~~~
The output is a tuple of two lists; peak times, peak events. The algorithm can be modified to return valley times and events. 
~~~~
'''
def threshold_algorithm(threshold_value, data):

    arrival_times = []
    peak_values = []
    maxtab, mintab = peakdet(data,threshold_value)
    
    for integer in range(0, len(maxtab)):
        arrival_times.append(maxtab[integer][0])
        peak_values.append(maxtab[integer][1])
    return arrival_times, peak_values

'''
`data` refers to any dataset that wishes to be cleaned up using a cross-correlation and smart threshold analysis. 

`template` refers to the list of points that will act as a template for cross correlation. 
The data that I used this function on was unpacked using `load_raw_data` function.

~~~
The output is a tuple of peak events, peak times, and the correlated data. 
~~~
'''
def clean_algorithm(data, template):
    template_list = template
    zero_convoluted_data = list(data)
    zero_noised_signal =   template_list

    a = zero_convoluted_data
    v = zero_noised_signal

    correlated_data = signal.correlate(a, v, mode = 'full' )
 
    bin_count = 1
    temp_data = []
    while 0 not in temp_data:
        temp_data, x = np.histogram(correlated_data, bins = bin_count)
        bin_count += 1
        
    hist, bin_edges = np.histogram(correlated_data, bins = bin_count)

    total_count = sum(hist)
    temp_sum = 0
    threshold_value = 0

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

    return final_peak_values, final_peak_times, correlated_data

'''
`times_data` should be a list of times that a photon has reflected back. 

This function attempts to make a mean-variance graph based on the discreet-time series data of photon arrivals. 
In other cases, it can be used to make a mean-variance graph of any discreet data. 
The mean-variance graph can be used to check if the data follows a poisson process, where the ***mean*** equals the ***variance***.
~~~~
The output is `mean_data, variance_data, std_data`, where `mean_data` is a list of all means, 
`variance_data` is a list of all variances, and `std_data` is a list of standard errors. 
Run `plt.plot(mean_data, variance_data)` and `plt.errorbar(mean_data, variance_data, yerr= std_data)` *(plt == matplotlib.pyplot)* to visualize the output. 
~~~~
'''
def mean_variance_graph(times_data):
    import numpy as np
    variance_data = []
    mean_data = []
    std_data = []
    for bin_count in range(50, 550, 50):
        events, edges = np.histogram(times_data,bins = bin_count)
        mean_data.append(np.mean(events))
        variance_data.append(np.std(events)**2)
        std_data.append(np.std(events)/float(len(events) ** 0.5))
    return mean_data, variance_data, std_data

'''
`sigma` refers to the standard deviation of the desired gaussian kernel. 

This function will take 401 points to create a full gaussian kernel. 
~~~~
The output is a gaussian kernel in a list (length of 401)
~~~~
'''
def gaussian_kernel(sigma):
    from scipy import stats
    import numpy as np
    x = np.arange(-200, 201)
    kernel = []

    for i in x:
		kernel.append(stats.norm.pdf(i, 0, sigma))
    return kernel

'''
`gold_standard_input` refers to the "true" data, the dataset that will be used to compare all other datasets. 

`algorithm_standard_input` refers to the "detected" data, the dataset that will be compared to the true dataset. 

`threshold_max` refers to the maximium threshold level the confusion matrix will work to. The **default** is 5. 

`threshold_interval` refers to the interval that the threshold levels will be increasing. The **default** is 0.15. 

(The last two functions only make sense if you are using this function in the context of peak_detection. If you are not doing so, feel free to modify the function.)

This function also will return the **matthew's correlation coefficient** which is a single value that measures the idealness of the algorithm. 

~~~~
The output is `matrix_set, matthews_coeff_set` as a tuple.
~~~~
'''
def make_confusion_matrix(gold_standard_input, algorithm_standard_input, threshold_max = 5, threshold_interval = 0.15):
    from sklearn.metrics import confusion_matrix, matthews_corrcoef
    import numpy as np
    matrix_set = []
    matthews_coeff_set = []
   
    if len(gold_standard_input) > len(algorithm_standard_input):
        gold_standard_input = gold_standard_input[0:len(algorithm_standard_input)]
    elif len(gold_standard_input) < len(algorithm_standard_input):
        algorithm_standard_input = algorithm_standard_input[0:len(gold_standard_input)]

    for criterion in np.arange(0., threshold_max, threshold_interval):
    
        algorithm_standard_cm = threshold_algorithm(criterion, algorithm_standard_input)
        gold_standard_cm = threshold_algorithm(0, gold_standard_input)
        algorithm_full_data_cm = np.zeros(len(algorithm_standard_input))
        gold_full_data_cm = np.zeros(len(gold_standard_input))

        algorithm_full_data_cm[algorithm_standard_cm] = 1
        gold_full_data_cm[gold_standard_cm] = 1

        matrix = confusion_matrix(gold_full_data_cm, algorithm_full_data_cm)
        true_positive = float(matrix[0][0])
        false_positive = float(matrix[0][1])
        false_negative = float(matrix[1][0])
        true_negative = float(matrix[1][1])
    
        matthews_coeff_set.append(matthews_corrcoef(gold_full_data_cm, algorithm_full_data_cm))
        matrix_set.append(matrix)
    return matrix_set, matthews_coeff_set

'''
`gold_standard_input`; please refer to the docstring for **make_confusion_matrix()**

`algorithm_standard_input`; again, ditto above

`threshold_max`; again, ditto above

`threshold_interval`; again, ditto above

The receiver operating curve is a visualization of the idealness of the algorithm. I ran this curve with my peak detection algorithms and poisson simulations as the `gold_standard_input`.

~~~~
The output is a tuple of false positives, true positives. But, the function calculates also false negatives and true negatives (just modify the output line).
~~~
'''
def receiver_operating_curve(gold_standard_input, algorithm_standard_input, threshold_max = 5, threshold_interval = 0.15):
    import numpy as np

    if len(gold_standard_input) > len(algorithm_standard_input):
        gold_standard_input = gold_standard_input[0:len(algorithm_standard_input)]
    elif len(gold_standard_input) < len(algorithm_standard_input):
        algorithm_standard_input = algorithm_standard_input[0:len(gold_standard_input)]
    
    false_positive_set = []
    true_positive_set = []
    threshold_value_set = []
    global gold_full_data, algorithm_full_data
    
    for criterion in np.arange(0, threshold_max, threshold_interval):
        true_positive = 0.
        false_positive = 0.
        true_negative = 0.
        false_negative = 0.
        false_positive_rate = 0.
        true_positive_rate = 0.
        
        algorithm_standard = threshold_algorithm(criterion, algorithm_standard_input)
        algorithm_full_data = np.zeros(len(algorithm_standard_input))
        algorithm_full_data[algorithm_standard] = 1
        
        gold_standard = threshold_algorithm(0, gold_standard_input)
        gold_full_data = np.zeros(len(algorithm_standard_input))
        gold_full_data[gold_standard] = 1
        
        threshold_value_set.append(criterion)
        
        for index in range(0, len(gold_full_data)):
            if algorithm_full_data[index] == 1:
                if gold_full_data[index] == 1:
                    true_positive += 1.
                else:
                    false_positive += 1.
            elif algorithm_full_data[index] == 0.:
                if gold_full_data[index] == 0:
                    true_negative += 1
                else:
                    false_negative += 1.
        
        true_positive_rate = true_positive/sum(gold_full_data)
        false_positive_rate = false_positive/(len(gold_full_data) - sum(gold_full_data))
        
        #print true_positive, false_positive, true_negative, false_negative, true_positive_rate, false_positive_rate
    
        false_positive_set.append(false_positive_rate)
        true_positive_set.append(true_positive_rate)
    return false_positive_set, true_positive_set

'''
`x` refers to the x coordinates.

`y` refers to the y coordinates.

~~~~
The output is a r-squared value based on a linear regression.
~~~~
'''
def rsquared(x, y):
    import scipy as sp
    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(x, y)
    return r_value ** 2

'''
`interval_data` refers to a list of times that a photon has reflected back.

`variable` is a counter: 1 to return variances, 2 to return means, and 3 to return standard errors. The **default** is 1, the variance. 

~~~~
The output is either the variance, the mean, or the standard error of the input list. (Modify the function to return tuples)
~~~~
'''
def statistics(interval_data, variable = 1):
    import numpy as np
    stats_mean = np.average(interval_data)
    stats_variance = np.var(interval_data)
    stats_stderror = np.std(interval_data)/(len(interval_data)**0.5)
    
    if variable == 2:
        return round(stats_variance, 3)
    elif variable == 3:
        return round(stats_stderror, 3)
    else:
        return round(stats_mean, 3)

'''
`expected` refers to the lambda of the poisson process. 

`trial` refers to how many times the poisson processs is going run to produce the expected value.

`repetition` refers to the number of times the poisson process is going to be repeated. The **default** is 1. 

The output is a list of three elements: [variances, means, standard errors]
***statistics() is used in this simulation***
'''
def full_simulation(expected, trial, repetition = 1):
    import numpy as np

    full_data = []
    final_statistics = []
    
    for i in range(0, repetition):
        data = poisson_interarrival(expected, trial)
        
        full_data.append(data)
    
    statistics_x = statistics(full_data, 1)
    statistics_y = statistics(full_data, 2)
    statistics_z = statistics(full_data, 3)
    
    final_statistics.append(round(np.mean(statistics_x), 3))
    final_statistics.append(round(np.mean(statistics_y), 3))
    final_statistics.append(round(np.mean(statistics_z), 3))
    
    return final_statistics

'''
`expected`; please refer to the docstring for **full_simulation()**

`trials`; again, ditto above

~~~~
The ouput is a list of times of poisson-modulated events.
~~~~
'''
def poisson(expected, trials):
    import numpy as np
    import random
    t = 0
    
    poisson_data = np.arange(0, trials, dtype = np.float)
    
    for i in range(1, int(trials) - 1):
        t += random.expovariate(expected)
        
        poisson_data[i] = t
        
    return poisson_data

'''
`expected`; please refer to the docstring for **full_simulation()**

`trials`; again, ditto above

~~~~
The output is a list of times in between poisson-modulated events.
~~~~
'''
def poisson_interarrival(expected, trials):
    import numpy as np

    data = [np.random.poisson(expected) for i in range(trials)]
    return data


