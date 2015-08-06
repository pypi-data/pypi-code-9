'''
plots and exports overlay images of speck channels with cell outlines, cell classes defined by colors
and cell labels
'''
import pickle
import ca_tracker.helper as h
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import ca_tracker.idaf_image_processing as iip
def loadTracklabelvol(exp_filename, resultsfolder):
    imdat = pickle.load(open(resultsfolder + exp_filename + '_trackdata.pickle', 'rb'))
    return imdat['track_labelvol']

def loadSpeckVolume(exp_filename, imagefolder):
    return h.loadTotalVolume(imagefolder + exp_filename + '_singlechannel/', 'sp', 2)

def loadClassInfo(exp_filename, resultsfolder):
    return pd.read_csv(resultsfolder + exp_filename + '_classes.csv')


def exportOverlaysWithLabels(exp_filename, config):


    resultsfolder = config['data_locations']['resultsfolder']
    imagefolder = config['data_locations']['imagefolder']

    overlay_savefolder = resultsfolder + exp_filename + '_labelOverlays/'
    try:
        os.mkdir(overlay_savefolder)
    except:
        pass    


    imvol = loadSpeckVolume(exp_filename, imagefolder)
    imvol = iip.softNormalize(imvol\
    ,alpha = config['visualization']['speck_brightness'], oneside = True)
    labelvol = loadTracklabelvol(exp_filename, resultsfolder)
    label_dat = loadClassInfo(exp_filename, resultsfolder) #classificaiton table

    labels_stable = label_dat[label_dat['is_stable']]
    
    labels_unstable = label_dat[~label_dat['is_stable']].label.tolist()
    labels_speck = labels_stable[labels_stable['is_specking']].label.tolist()
    labels_hom = labels_stable[~labels_stable['is_specking']].label.tolist()

    for i in range(labelvol.shape[0]):
        print 'save labelOverlay for frame nr %s to %s' % (str(i), overlay_savefolder)
        label_mat = labelvol[i,:,:]
        im = imvol[i,:,:]
        
        #get outlines, centroids and labels for different object classes
        objects_hom = h.getCentroidsAndBoundariesForLabels(label_mat, labels_hom)
        objects_speck = h.getCentroidsAndBoundariesForLabels(label_mat, labels_speck)
        objects_unstable = h.getCentroidsAndBoundariesForLabels(label_mat, labels_unstable)
        sns.set_style("white")
        plt.close()
        fig, ax = plt.subplots(1,1)
        plotOverlayOnImage(ax, im, objects_hom, objects_speck, objects_unstable)

        savename = overlay_savefolder + 'labelOverlays_' + str(i) + '.png'
        fig.savefig(savename,dpi=300)


    
def plotLabelsAndOutlines(ax, dat, color):
    for i in range(len(dat['boundaries'])):
        ax.plot(dat['boundaries'][i][:,1], dat['boundaries'][i][:,0], color)
    for i in range(len(dat['centroids'])):
        ax.text(dat['centroids'][i,1], dat['centroids'][i,0],str(int(dat['labels'][i]))\
            , color='y', horizontalalignment='center', verticalalignment='center', fontsize=5)
        


def plotOverlayOnImage(ax, im, objects_hom, objects_speck, objects_unstable):
    
    ax.imshow(im, cmap='gray')
    plotLabelsAndOutlines(ax,objects_hom, 'g')
    plotLabelsAndOutlines(ax,objects_speck, 'r')
    plotLabelsAndOutlines(ax,objects_unstable, 'b')

