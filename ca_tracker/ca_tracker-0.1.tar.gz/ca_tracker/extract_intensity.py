import pandas as pd 
import pickle
#import config 
import helper as h
import numpy as np
import os


def measureIntPerFramePerLabel(exp_filename, labelvol, times, max_frames, imagefolder):
	
	dict_mint = {}
	dict_frames = {}

	labels_all = np.unique(labelvol.flatten())[1:]

	


	#init dict
	for label in labels_all:
		dict_mint[label] = []
		dict_frames[label] = []


	
	for i in range(max_frames):
		progress = i/float(max_frames) * 100.
		

		path = imagefolder + exp_filename + '_singlechannel/' + times.filename[i] + '_c001.tif'
		print 'measure ca intensity of ' + os.path.basename(path) +  ' ' + str(progress) + ' percent done'
		
		im = h.loadImage(path)
		labelvol_index = times.frames_to_sp[i]
		label_mat = labelvol[labelvol_index,:,:]

		labels = np.unique(label_mat.flatten())[1:]

		for label in labels:
			pixels = im[label_mat==label]
			if len(pixels) == 0:
				mean_int = np.nan
			else:
				mean_int = np.mean(pixels)
			dict_mint[label].append(mean_int)
			dict_frames[label].append(i)
	return dict_mint, dict_frames		


#exp_filenames = ['75ms_7p5_1', '75ms_7p5_2', '50ms_7p5_1', '50ms_7p5_2']

#exp_filenames = ['50ms_7p5_1']

def extract_intensity(exp_filename, config):

	#data import
	times = pd.read_csv(config.resultsfolder + exp_filename + '_timetable.csv')
	classes = pd.read_csv(config.resultsfolder + exp_filename + '_classes.csv')
	imdat = pickle.load(open(config.resultsfolder + exp_filename + '_trackdata.pickle', 'rb'))
	labelvol = imdat['track_labelvol'].astype(int)


	#measure intensity frame by frame
	max_frames = times['filename'].count()
	d_mint, d_frames = measureIntPerFramePerLabel(exp_filename, labelvol, times, max_frames, config.imagefolder)


	#convert dict data tp data tables
	dat = pd.DataFrame(index=times.index)
	for label in d_mint.keys():
		dat[label] = pd.Series(d_mint[label], index=d_frames[label])

	classes_stable = classes[classes.is_stable]
	labels_speck = classes_stable[classes_stable.is_specking]['label'].tolist()
	labels_hom = classes_stable[~classes_stable.is_specking]['label'].tolist()


	#divide into specking and non specking cells
	dat_speck = dat[labels_speck] #intensity data per frame for specking cells
	dat_hom = dat[labels_hom] #intensity data per frame for homogeneous cells

	#export data
	dat_speck.to_csv(config.resultsfolder + exp_filename + '_intensities_speck.csv')
	dat_hom.to_csv(config.resultsfolder + exp_filename + '_intensities_hom.csv')

















