
import numpy as np
import skimage.filter as skfilter
import skimage.morphology as skmorph
import skimage.measure as skmeasure
from skimage.feature import peak_local_max

import scipy.ndimage
#if not hasattr(skfilter, 'gaussian_filter'):
#	skfilter.gaussian_filter = scipy.ndimage.gaussian_filter


"""
this package contains routines for basic image processing on numpy arrays

-watersheds
-threshold computations

"""


def gaussian_blur(im, blur):
    '''
    wrapper for gaussian_filter from skimage.
    since skimage can only deal with folating images in range -1 to 1, the wrapper
    normalizes each image from 0 to 1 and rescales back to original scale.
    '''
    
    
    im_data_type = im.dtype
    
    #normalize image to achieve floating values between 0 and 1
    maximum = np.max(flattenImage(im))
    im_n = im/float(maximum)

    #apply gaussian filter and scale to original
    im_filtered = skfilter.gaussian_filter(im_n, blur) * maximum

    return im_filtered.astype(im_data_type)





def softNormalize(im,alpha = 0, oneside = False):
    """
    normalizes the image to the alpha and 1-alpha percentiles

    :param im: input image
    :param alpha: percentile to define min and max value to normalize
    :param oneside: if true, the distrubution is only cut in the upper part

    """ 
    flattened = flattenImage(im)
    max = np.percentile(flattened, (1-alpha)*100)
    if oneside: #one-sided cutting of percentile
        min = np.min(flattened)
    else: #two-sided cutting of percentile
        min = np.percentile(flattened,alpha*100)    
    normed = (im-min)/(max-min)
    normed[normed<0] = 0
    normed[normed>1] = 1
    return normed

def flattenImage(im):
    """
    reduces an numpy array image to one dimension.
    """ 
    return np.reshape(im,np.product(im.shape)) 



def findSignificantLocalMaxima(im,min_distance = 10,sig_thresh = 2, radius = 15, quantile = 0.5):
    """
    moehl 2014, idaf, dzne bonn

    returns significant local maxima as integer labels in matrix

    All detected local maxima have to pass a significance test: Their value has to be sig_thresh times higher than the 
    reference intensity Iref of the local neighborhood. Iref is defined as the user-defined 
    quantile (default: median) of intensities if the local neighborhood

    :param im: input image
    :param min_distance: minimal distance between two maxima
    :param sig_thresh: significance value, raise this value to increase the stringency for significant peaks
    :param radius: the radius of the neighborhood in which the reference intensity is calculated
    :param quantile: defines the value of the reference intensity
    """
    

    
    maxima = findLocalMaxima(im, min_distance = min_distance) #find seedpoints
    im16bit = to16bit(im)
    iref = skfilter.rank.percentile(im16bit, skmorph.disk(radius),  p0=quantile) #percentile filter to claculate referecne intensity of local neighborhood

    sig = im16bit.astype('float')/iref.astype('float') #significance value
    maxima[sig<sig_thresh]=0 # remove all maxima below the significance value
    
    return maxima


def findLocalMaxima(im, min_distance = 10):
    """
    returns local maxima as integer labels in matrix

    :param im: input image
    :param min_distance: minimal distance between two maxima
    """
    markers = np.zeros([im.shape[0],im.shape[1]], dtype = 'int16')
    markers[peak_local_max(im.astype('float'),indices = False, min_distance = min_distance)] = 1
    return skmorph.label(markers)



def gradientWeightedDistanceTransform(mask, img, blur, gradient_weight, object_size=None):
    
    dist = distanceTransform(mask, object_size=object_size)
    grad = gradientImage(img, blur)
    
    return weigthtDistanceImByGradientIm(dist, grad, gradient_weight)



def distanceTransform(mask, object_size=None):

    _, dist =  skmorph.medial_axis(mask, mask=None, return_distance=True) #distance transform
        
    if object_size is not None: #if object size is given, the distanceTransform is modulated by a sinus with width of the object size
        dist_max = object_size
        dist = np.abs(np.sin(2*np.pi*dist/2/dist_max)*np.minimum(dist, dist_max))
    return dist

def gradientImage(img, blur):
    return skfilter.prewitt(gaussian_blur(img, blur).astype('float')) #gradient transform

def weigthtDistanceImByGradientIm(dist, grad, gradient_weight):
    grad_normed = (grad - np.min(grad))/(np.max(grad) - np.min(grad))
    return dist * np.exp(1-grad_normed*gradient_weight) #gradient weigthed distance map




def watershed(mask,im = None, method = 'distanceTransform',
                blur = 0, markers = None, gradient_weight = 1,
                output_watershed_image = False, object_size = None):
    """
    moehl 2014, dzne bonn, idaf

    returns a label matrix computed by different watershed methods:
    
    distanceTransform: standard watertshed based on distance transform of mask
    
    gradientImage: based on gradient of im. This method is useful, if you have
    e.g. a membrane staining
    
    gradientWeightedDistance: mixture of gradient image and distance map. The
    influence of the gradient can be adjusted with gradient_weigtht
    (1= original weight as described in the referecne)

    inputImage: watershed is applied directly to input image im 

    :param mask: binary image (boolean matrix) to define foreground and background
    :param im: gray value image, needed for all methods except distanceTransform
    :param blur: sigma of gaussian filter to smooth the gradient image (method
        geadientImage and gradientWeightedDistance) or the input image (method
        inputImage) 
    :param markers: label matrix of integers defining watershed seedpoints.
        If none, local maxima of the watershed input are computed as seedpoints
    :param gradientWeight: only relevant for method gradientWeightedDistance.
        Adjusts the weight of the gradient image.
    :output_watershed_image: if True, the label matrix and the input image of
        the watershed are returned. If False, only the label matrix is returned.
    :param object_size: approx. size of objects to segment. If given, this value
        transforms the distance map by a sinus of width object_size (don't use
        this parameter for standard segmentatations)


    REFERENCE for gradientWeightedDistanceTransform method: 
    
    Gang Lin, Umesh Adiga, Kathy Olson, John F. Guzowski, Carol A. Barnes, and
    Badrinath Roysam
    A Hybrid 3-D Watershed Algorithm Incorporating Gradient Cues & Object
    Models for Automatic Segmentation of Nuclei in Confocal Image Stacks
    Vol. 56A, No. 1, pp. 23-36 Cytometry Part A, November 2003.
    """
    
    def distanceTransform_outer():
        return distanceTransform(mask, object_size=object_size)
        

    def gradientImage_outer():
        return gradientImage(im, blur)#gradient transform
        

    def gradientWeightedDistance_outer():
        return gradientWeightedDistanceTransform(mask\
                                    , im, blur, gradient_weight\
                                    , object_size=object_size)
    
    def inputImage():
        return gaussian_blur(im, blur).astype('float')
        
    

    methods = {'distanceTransform': distanceTransform_outer\
                , 'gradientImage': gradientImage_outer\
                , 'gradientWeightedDistance': gradientWeightedDistance_outer\
                , 'inputImage': inputImage\
                }


    try: 
        waterIn = methods[method]()
    except AttributeError:
        raise Exception('method ' + method + ' needs pixelimage (im) as input') 
        
    if markers is None:
        markers = findLocalMaxima(waterIn) #find seedpoints
    
    labels = skmorph.watershed(-waterIn, markers, mask = mask)  #perform watershed

    if output_watershed_image: #return label matrix and the input image of the watershed (waterIn)
        return labels, waterIn

    return labels       






def to8bit(im, percentile = 0.):
        im = softNormalize(np.array(im),percentile)*256
        im[im<0] = 0
        im[im>255] = 255
        return im.astype('uint8')

def to16bit(im, percentile = 0.):
        im = softNormalize(np.array(im),percentile)*65536
        im[im<0] = 0
        im[im>65536] = 65536
        return im.astype('uint16')      




def removeLabels(labelmatrix,min_obj_size,max_obj_size):
    '''
    from a given label matrix connected components are removed that are smaller than min_obj_size
    and larger than max_obj_size
    moehl 2014

    :param labelmatrix: labelmatrix of integers
    :type: 2D numpy array of integers
    :param min_obj_size: minimal object size in pixels
    :param max_obj_size: maximal object size in pixels  
    '''
    if min_obj_size > 0:    
        labelList = np.unique(labelmatrix)[1:]  # list of all labels
        for i in labelList:
            if (len(labelmatrix[labelmatrix == i]) < min_obj_size) or (len(labelmatrix[labelmatrix == i]) > max_obj_size):  # check object size
                labelmatrix[labelmatrix == i] = 0 # remove small objects
        return skmorph.label(labelmatrix) # make new label enumeration for remaining objects 
    return labelmatrix


def removeSmallLabels(labelmatrix,min_obj_size):
    '''
    from a given label matrix connected components are removed that are smaller than min_obj_size
    moehl 2014

    :param labelmatrix: labelmatrix of integers
    :type: 2D numpy array of integers
    :param min_obj_size: minimal object size in pixels 
    '''
    return removeLabels(labelmatrix,min_obj_size,float('inf'))


def localThreshBernsen(im,corr = 1,
    radius = 15, smooth = 0, alpha = 0,
    local_contrast_thresh = 0.06, midgray_thresh = 0.5, hard_min_thresh = 0):
    '''
    local thresholding with bernsen method
    moehl 2014
    see http://fiji.sc/wiki/index.php/Auto_Local_Threshold for further explanation

    :param im: input image
    :type: im 2Dnumpy array
    :param corr: correction factor to raise or lower the calculated thresholds, if 1, threshold is not corrected  
    :param radius: radius of local neighborhood where thresh is calcultated
    :param smooth: sigma of gaussian filter used to smooth the image before thresholding
    :param alpha: quantile that is used to calculate "soft minimum" and "soft maximum", if 0 "hard" min and max are calculated
    :param local_contrast_thresh: local contrast threshold, to classify image in high- and low contrast regions (only high contrast regions have local threshold)
    :param midgray_thresh: midgray threshold, global threshold that is used in ,low contrast regions
    :param hard_min_thresh: use this (global) threshold to exclude dark regions 
    '''


    im_filtered = to8bit(gaussian_blur(im, smooth)) #smoothed image
    im = to8bit(im)

    #raise('err')

    soft_min = skfilter.rank.percentile(im,skmorph.disk(radius),p0 = alpha) # lower percentile filter
    soft_max = skfilter.rank.percentile(im, skmorph.disk(radius),p0 = 1 - alpha) # higher percentile filter

    local_contrast =  soft_max - soft_min
    midgray = np.dstack((soft_min,soft_max)).mean(axis = 2) #average of soft_min and soft_max

    low_cont = local_contrast/256.0 < local_contrast_thresh
    high_cont = local_contrast/256.0 >= local_contrast_thresh


    mask = ((midgray > midgray_thresh*256.) & low_cont) | ((im_filtered  > midgray * corr) & high_cont)
    return mask & (im_filtered > hard_min_thresh *256.)




def bwboundaries(labelmatrix):
    labels = np.unique(labelmatrix)[1:]
    
    contours = []
    for i in range(len(labels)):
        label = labels[i]
        lmat = labelmatrix.copy()
        lmat[lmat!=label] = 0
        contour = skmeasure.find_contours(lmat, 0)
        contours = contours + contour
    
    return contours




