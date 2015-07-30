import json

with open('config.json') as data_file:
        	conf_data = json.load(data_file)

dt_ca = conf_data['image_time_intervals']['dt_ca']#2 #time interval of figh frequencey timeseries (2 channel)
dt_sp = conf_data['image_time_intervals']['dt_sp']#5*60 # time interval of final timeseries to monitor specking(3 channel)

#image locations
resultsfolder = conf_data['data_locations']['resultsfolder']#'../../../results/tst_2/' 
imagefolder = conf_data['data_locations']['imagefolder']#'../../../data/2nd_test_data/shortnames/'





#analysis parameters

#cell detection
bg_thresh = conf_data['cell_detection']['bg_thresh']#0.3 #background threshold on probability map
weight = conf_data['cell_detection']['weight']#5 #weight of distance image
prob_smooth = [1, 1.5, 1.5] #zyx gauss filter sigma values


n_frames_min = conf_data['classification']['n_frames_min']# 11 #minimum nr of frames of a cell object
max_area_change_thresh = conf_data['classification']['max_area_change_thresh']#0.5 # decrease to sort out more cells that have unstable shape over time
spot_thresh = conf_data['classification']['spot_thresh']#4.6#6 # increase to be more stringent for aggregation

#vis parameters
speck_brightness = conf_data['visualization']['speck_brightness']#0.001 # increase to get brighter images of spack channel
#median_filter_size = 4

