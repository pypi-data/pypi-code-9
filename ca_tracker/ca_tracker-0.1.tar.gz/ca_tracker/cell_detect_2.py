import sys
sys.path.append('/home/moehlc/idaf_library')

import libidaf.idaf_image_processing as iip
import matplotlib.pyplot as plt
import numpy as np

import helper as h
import skimage.filter as flt
import skimage.morphology as morph
import skimage.segmentation as seg
import os
from sklearn.cluster import KMeans
import pickle
from PIL import Image
from multiprocessing import Process
import config

def segmentCells(im_sm, im, bg_thresh, weight, min_distance=2):
	msk = im_sm > bg_thresh	
	dist = iip.distanceTransform(msk, object_size=None) #distance transform
	dist_sm = flt.gaussian_filter(dist, sigma=[1,1]) #smoothed distance transform
	prob_weight_dst = np.exp(im_sm*weight)*dist_sm #probability weighted distance trafo   

	#find cell seeds based on probability weigthed distance trafo
	seed_msk = iip.findLocalMaxima(prob_weight_dst, min_distance = min_distance)
	
	#watershed with seeds and probability image
	return  iip.watershed(msk,im = im, method = 'inputImage',
	                blur = 0, markers = seed_msk), seed_msk



def saveOverlays(labels, seed_msk,im_b, frame_nr, xy_range, savefolder):
	
	if xy_range is not None:
		xmin= xy_range[0]
		xmax = xy_range[1]
		ymin = xy_range[2]
		ymax = xy_range[3]
	else:
		xmin=0
		xmax= labels.shape[0]
		ymin=0
		ymax= labels.shape[1]

		
	seed_k = np.nonzero(seed_msk[xmin:xmax, ymin:ymax]) #seed coordinates

	bnd = h.contoursFromMask(labels[xmin:xmax,ymin:ymax])
	plt.close()
	f1, axes1 = plt.subplots(1,1)
	axes1.imshow(im_b[xmin:xmax,ymin:ymax], cmap='gray')
	axes1.plot(seed_k[1], seed_k[0],'+y')
	for bn in bnd:
		axes1.plot(bn[:,1], bn[:,0],'y')

	savename = savefolder + 'brightseg_' + str(frame_nr) + '.png'
	try:
		os.mkdir(savefolder)
	except:
		pass	
	f1.savefig(savename,dpi=300)


def getLabels(label_mat):
    labels = np.unique(label_mat)
    return labels[1:]

def getCentroids(label_mat):
    labels = getLabels(label_mat)
    xc = []
    yc = []
    for label in labels:
        coor = np.nonzero(label_mat == label)
        xc.append(np.mean(coor[0]))
        yc.append(np.mean(coor[1]))

    centroids  = np.array([xc, yc])
    return centroids.swapaxes(0,1)  

def generateCentroidMat(label_mat):
	centroids = getCentroids(label_mat)
	cmat = np.zeros(label_mat.shape)
	for centroid in centroids:
		cmat[np.round(centroid[0]), np.round(centroid[1])] = 256
	return cmat	

def save_centroid_images(ll, savefolder):
	try:
		os.mkdir(savefolder)
	except:
		pass	
	for i in range(len(ll)):
		print 'export centroid image nr ' + str(i)
		labelmat = ll[i]
		cmat = generateCentroidMat(labelmat)
		im = Image.fromarray(cmat)
		filename = savefolder + 'centroids_' + str(i) + '.tif'
		im.save(filename)




def segment_ts(bg_thresh, weight, prob_smooth, exp_filename, loadfolder, savefolder=None, xy_range=None):

	ll = [] #list of label matrices

	#import
	#normalize probability image
	vol = h.loadVolume_inner(loadfolder + exp_filename + '_rgb/', ['cell_probability'])
	vol = vol.astype(float)/max(vol.flatten())
	#smooth probability image
	vol_sm = flt.gaussian_filter(vol, sigma=prob_smooth)
	#load brightfield image
	vol_b = h.loadTotalVolume(loadfolder + exp_filename + '_singlechannel/', 'sp', 3) #brightfield channel




	n_frames = vol.shape[0]
	print 'start cell object detection of file %s' % exp_filename
	for i in range(n_frames):
		print 'detecting cell objects in frame nr %s' % str(i)
		im = vol[i,:,:]
		im_b = vol_b[i,:,:]
		im_sm = vol_sm[i,:,:]#flt.gaussian_filter(im, sigma=[1.5,1.5])
		
		labels, seed_msk = segmentCells(im_sm, im, bg_thresh, weight)	
		ll.append(labels)
		if savefolder is not None:
			overlay_savefolder = savefolder + exp_filename + '_overlays/'
			saveOverlays(labels, seed_msk, im_b,i, xy_range, overlay_savefolder)
			print 'save overlay for frame nr %s to %s' % (str(i), savefolder)

	return ll		
	

def process_datset(exp_filename, bg_thresh, weight, prob_smooth, loadfolder, savefolder):
	print 'start segmentation of ' + exp_filename

	ll = segment_ts(bg_thresh, weight, prob_smooth, exp_filename, loadfolder, savefolder=savefolder, xy_range=None)
	data = {\
		'exp_filename' : exp_filename\
		,'loadfolder' : os.path.abspath(loadfolder)\
		,'bg_thresh' : bg_thresh\
		, 'weight' : weight\
		, 'prob_smooth' : prob_smooth\
		, 'labels' : ll
	}

	
	pickle.dump(data, open(savefolder + exp_filename + '_segdata.pickle', 'wb'))
	save_centroid_images(ll, savefolder + exp_filename+ '_centroids/')










def cell_detect_2(exp_filename, config):

	process_datset(exp_filename, config.bg_thresh, config.weight, config.prob_smooth, config.imagefolder, config.resultsfolder)
	#p = Process(target=process_datset, args = [exp_filename, bg_thresh, weight, prob_smooth, loadfolder, savefolder])
	#p.start()
	print 'start segmentation of ' + exp_filename

	









