import pandas as pd 
#import config
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import helper as h
import pickle
import sys
sys.path.append('/home/moehlc/idaf_library')
import libidaf.idaf_image_processing as iip

def markUnstableCells(label, max_area_diffs, thresh):
    if max_area_diffs[label] > thresh:
        return False
    return True 

def markSpeckingCells(label, max_specking, thresh):
    
    if max_specking[label] > thresh:
        return True
    return False


def classifyUnstableCells(dat, thresh):
    dat['area_diff'] = dat.groupby('label')['area'].transform(pd.Series.diff) #area_diffs per frame

    grouped = dat.groupby(['label'])

    #max area changes relative to mean area
    max_area_diffs =  grouped['area_diff'].max() / grouped['area'].mean()

    # classify unstable cells as unstable
    dat['is_stable'] = dat.apply(lambda row: markUnstableCells(\
         row['label'],max_area_diffs,thresh), axis=1)

    return dat

def classifySpeckingCells(dat, thresh):
    grouped = dat.groupby(['label'])
    max_specking = grouped['rel_max_s'].max() #maximum value of hessian determinant max
    dat['is_specking'] = dat.apply(lambda row: markSpeckingCells(\
         row['label'], max_specking,thresh), axis=1)
    return dat

def getPlottingDataByClassname(dat, class_name, feature_name, yesno = True):
    labels = np.unique(dat['label'].tolist())
    y = []
    for label in labels:

        sel = dat[dat['label'] == label]
        if sel[class_name].all() and yesno:   
            y.append(sel[feature_name].tolist())
        if not  sel[class_name].all() and not yesno:
            y.append(sel[feature_name].tolist())

    times = np.array(sel['time_abs'].tolist())

    return y, times



def plotTsClasses(dat,ax, filter_col, feature, xlabel=False, ylabel=None):
    y_agg, time = getPlottingDataByClassname(dat,filter_col, feature)
    y_hom, time = getPlottingDataByClassname(dat,filter_col, feature, yesno = False)
    time = time/60 #time in minutes
    if len(y_agg)>0:
        sns.tsplot(y_agg, time=time, err_style="unit_traces", color = 'r', ax = ax, estimator=np.nanmean) 
    if len(y_hom)>0:
        sns.tsplot(y_hom, time=time, err_style="unit_traces", color = 'b', ax = ax, estimator=np.nanmean)         
    if xlabel:
        ax.set_xlabel('time [min]')
    if ylabel is not None:
        ax.set_ylabel(ylabel)
            

def plot_graphs(dat, savepath=None):
    cv = []
    un = []
    plt.close()
    fig, ax = plt.subplots(2,1)
    #plotTsClasses(dat,ax[0], 'is_specking'\
    #    , 'cv_s', xlabel=False, ylabel='cv contrast asc channel')
    #ax[0].set_ylim([0, 1])
    plotTsClasses(dat,ax[0], 'is_specking'\
        , 'rel_max_s', xlabel=True, ylabel='specking_measure')

    plotTsClasses(dat,ax[1], 'is_stable'\
        , 'area', xlabel=True, ylabel='cell area [pixels]')

    
    #ax[2].set_ylim([0, 1.5])
    if savepath is not None:
        savefolder = os.path.dirname(os.path.abspath(savepath))
        try:
            os.mkdir(savefolder)
        except:
            pass
        fig.savefig(savepath)   

    return fig    


def exportOverlayImages(labelvol, resultsfolder, imagefolder, exp_filename, label_dat, speck_brightness):
    vol_b = h.loadTotalVolume(imagefolder + exp_filename + '_singlechannel/', 'sp', 2) #speck channel
    n_frames = vol_b.shape[0]
    vol_bright = iip.softNormalize(vol_b,alpha = speck_brightness, oneside = True)
    for i in range(n_frames):
        
        im_b = vol_bright[i,:,:]
        #im_b = vol_b[i,:,:]
        labels = labelvol[i,:,:]
            
        overlay_savefolder = resultsfolder + exp_filename + '_speckOverlays/'
        sns.set_style("white")
        saveOverlays(labels, im_b, i, overlay_savefolder, label_dat)
        print 'save overlay for frame nr %s to %s' % (str(i), overlay_savefolder)


def saveOverlays(label_mat, im_b, frame_nr, savefolder, label_dat):
    #labels = label_dat['label'].tolist() 
    

    
    plt.close()
    f1, axes1 = plt.subplots(1,1)
    

    
    axes1.imshow(im_b, cmap='gray')
    #axes1.imshow(im_b)
    labels_stable = label_dat[label_dat['is_stable']]

    labels_speck = labels_stable[labels_stable['is_specking']].label.tolist()
    labels_hom = labels_stable[~labels_stable['is_specking']].label.tolist()
    speck_bnds = h.getBoundariesForLabels(label_mat, labels_speck)
    hom_bnds = h.getBoundariesForLabels(label_mat, labels_hom)

    for bn in speck_bnds:
        axes1.plot(bn[:,1], bn[:,0],'r')
    for bn in hom_bnds:
        axes1.plot(bn[:,1], bn[:,0],'g')    
        
    savename = savefolder + 'trackseg_' + str(frame_nr) + '.png'
    try:
        os.mkdir(savefolder)
    except:
        pass    
    f1.savefig(savename,dpi=300)



#exp_filenames = ['75ms_7p5_1', '75ms_7p5_2', '50ms_7p5_1', '50ms_7p5_2']
#exp_filenames = ['50ms_7p5_1']


def classify_cells(exp_filename, config):
    #exp_filename = '50ms_7p5_2'
    #xp_filename = '75ms_7p5_1'

    dat = pd.read_csv(config.resultsfolder + exp_filename + '_features.csv')
    dat = classifyUnstableCells(dat, config.max_area_change_thresh)
    dat = classifySpeckingCells(dat, config.spot_thresh)

    dat_classes = dat[['label', 'is_specking', 'is_stable']].drop_duplicates()
    dat_classes.to_csv(config.resultsfolder + exp_filename + '_classes.csv')


    savepath_plots = config.resultsfolder + exp_filename + '_plots/' + exp_filename + '_specking_area.pdf'
    fig = plot_graphs(dat, savepath=savepath_plots)


    imdat = pickle.load(open(config.resultsfolder + exp_filename + '_trackdata.pickle', 'rb'))
    labelvol = imdat['track_labelvol']

    exportOverlayImages(imdat['track_labelvol'],\
             config.resultsfolder, config.imagefolder, exp_filename, dat_classes, config.speck_brightness)














