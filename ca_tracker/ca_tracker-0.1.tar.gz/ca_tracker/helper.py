#import sys
#sys.path.append('/home/moehlc/idaf_library')
#sys.path.append('/mnt/moehlc/home/idaf_library')
import idaf_io as iio
#import libidaf.image_importer as ip 
import idaf_image_processing as iip
import numpy as np
import os
#import vigra
import logging
import skimage.filter as flt
import skimage.morphology as morph
from skimage import io

def loadImage(path):
    im = loadTiff2PixelChannel(path)
    return np.squeeze(im)




def loadTiff2PixelChannel(channel_filename):
    '''
    reads a single tiff image and returns a PixelChannel
    '''
    
    absname = os.path.abspath(str(channel_filename))
    
    #n_images = vigra.impex.numberImages(absname)
    
    #if n_images != 1:
    #    logging.info('more than one image in file ' + absname)
    #    return
    
    logging.info("Loading '%s' with skimage...", absname)
    #return vigra.readImage(absname, dtype='FLOAT')
    return io.imread(absname)





def loadVolume_inner(path, pattern):
    filenames = iio.getFilelistFromDir(path,pattern)
    filenames.sort()
    print 'detected list of files:'
    print filenames

    name = filenames[0]
    im = loadImage(path+name)
    n_frames = len(filenames)
    n_y = im.shape[0]
    n_x = im.shape[1]

    vol = np.zeros([n_frames,n_y, n_x])
    print 'vol_shape'
    print str(vol.shape)
    for frame in range(n_frames):
        name = filenames[frame]
        vol[frame,:,:] = loadImage(path+name)

    return vol.astype('uint16') 





def loadVolume(path, module_name, channel):
    
    pattern = [module_name + '_t', 'c00' + str(channel), '.tif']

    return loadVolume_inner(path, pattern)

def loadTotalVolume(path, module_type, channel):
    module_names = getModuleNames(path, module_type=module_type)

    vol = loadVolume(path, module_names[0], channel)

    for name in module_names[1:]:
        akt_vol = loadVolume(path, name, channel)
        vol = np.concatenate((vol, akt_vol), axis=0)

    return vol  



def contoursFromMask(msk):
    labelmat = morph.label(msk)
    labelmat[labelmat==0] = np.max(labelmat.flatten())+1
    labelmat[msk==False]=0
    return iip.bwboundaries(labelmat)



def getModuleNames(path, module_type=None):
    pattern = ['_c00', '.tif']
    names = iio.getFilelistFromDir(path,pattern)
    for i in range(len(names)):
        names[i] = names[i][:4]
    
    module_names = np.unique(names)

    if module_type is None:
        return module_names

    return [k for k in module_names if module_type in k]


def getBoolmatForLabels(labelmat, labels):
    '''
    give a label matrix and a list of labels and get a boolean matrix with
    True where any of the labels is present
    ''' 
    boolmap = labelmat != labelmat
    for label in labels:
        tmp = labelmat==label
        boolmap = np.any(np.array([boolmap, tmp]), axis=0)
    return boolmap



def getBoundariesForLabels(labelmat, labels):
    '''
    give a label matrix and a list of labels and get a list of boundary coordinates
    '''
    boolmat = getBoolmatForLabels(labelmat, labels)

    labelmat_clean = labelmat.copy()
    labelmat_clean[~boolmat] = 0
    
    return iip.bwboundaries(labelmat_clean)



