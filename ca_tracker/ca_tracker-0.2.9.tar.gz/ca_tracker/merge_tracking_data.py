import pandas as pd 
import pickle
import numpy as np
import ca_tracker.helper as h
import matplotlib.pyplot as plt
import os





def filterTrajectories(tdat, n_frames):
    '''
    only keep trajectories with minimal length of n_frames and starting at frame 0
    '''
    out  = pd.DataFrame(columns=tdat.columns) #init new empty dataframe
    newlabel = 1 #counter for new labels
    for k,g in tdat.groupby('Trajectory'):
        #g is a dataframe with entries all sharing the same label
        if (len(g['x'].tolist()) >= n_frames) and g.Frame.min() == 0:
            g['Trajectory'] = newlabel #assign new label and append if n_frames or more and first frame is 0
            newlabel += 1
            out = out.append(g) 
    return out   


def removeTrajectoriesWithZeroLabel(tdat):
    '''
    only keep trajectories with no zero label (==background) 
    '''
    out  = pd.DataFrame(columns=tdat.columns) #init new empty dataframe
    newlabel = 1 #counter for new labels
    for k,g in tdat.groupby('Trajectory'):
        #g is a dataframe with entries all sharing the same trajectory label
        if g.old_label.min() != 0:
            g['Trajectory'] = newlabel #assign new label and append if n_frames or more and first frame is 0
            newlabel += 1
            out = out.append(g) 
    return out      



def labelByTrajectory(newlabel, t_act, labelvol_new,labelmats):
    for i in range(len(t_act['Frame'])):
        frame = t_act['Frame'][i]
        x = round(t_act['x'][i])
        y = t_act['y'][i]

        labelmat = labelmats[frame]
        label = labelmat[y,x]
        #print 'old label: ' + str(label)
        labelmat_new = labelmat*0
        labelmat_new[labelmat==label] =  newlabel
        #print 'new label: ' + str(newlabel)
        labelvol_new[frame,:,:] = labelmat_new
    return labelvol_new 

def findLabel(frame, x, y, labelmats):
    return labelmats[int(frame)][int(y),int(x)]


def assignLabels(tsel, labelmats):
    tsel['old_label'] = tsel.apply(lambda row: findLabel(row['Frame']\
        , row['x'],row['y'], labelmats), axis=1)
    return tsel 

def setNewLabel(labelmats_old, labelvol_new, label_new, label_old, frame):
    #print 'update trajectory %s to labelmatrix' % str(label_new)
    frame = int(frame)
    
    labelmat_old = labelmats_old[frame]
    mask = labelmat_old == label_old
    labelmat_new = labelvol_new[frame,:,:]
    labelmat_new[mask] = label_new
    labelvol_new[frame,:,:] = labelmat_new

def computeNewLabelVol(tsel, labelmats):
    labelvol_new = np.zeros([len(labelmats), labelmats[0].shape[0], labelmats[0].shape[1]])
    tsel.apply(lambda row: setNewLabel(labelmats, labelvol_new\
        , row['Trajectory'], row['old_label'], row['Frame']), axis=1)
    return labelvol_new


def saveOverlays(labels, im_b, frame_nr, savefolder):
    
    bnd = h.contoursFromMask(labels)
    plt.close()
    f1, axes1 = plt.subplots(1,1)
    axes1.imshow(im_b, cmap='gray')
    for bn in bnd:
        axes1.plot(bn[:,1], bn[:,0],'y')

    savename = savefolder + 'trackseg_' + str(frame_nr) + '.png'
    try:
        os.mkdir(savefolder)
    except:
        pass    
    f1.savefig(savename,dpi=300)

def exportOverlayImages(labelvol, resultsfolder, imagefolder, exp_filename):
    vol_b = h.loadTotalVolume(imagefolder + exp_filename + '_singlechannel/', 'sp', 3) #brightfield channel
    for i in range(vol_b.shape[0]):
        
        im_b = vol_b[i,:,:]
        
        
        labels = labelvol[i,:,:]
        
        
        overlay_savefolder = resultsfolder + exp_filename + '_tracksegOverlays/'
        saveOverlays(labels, im_b, i, overlay_savefolder)
        print 'save overlay for frame nr %s to %s' % (str(i), overlay_savefolder)

    

def merge_tracking_data(exp_filename, config):

    resultsfolder = config['data_locations']['resultsfolder']
    imagefolder = config['data_locations']['imagefolder']


    tdat = pd.read_csv(resultsfolder + exp_filename + '_trajectories.csv')
    tdat = tdat[['Trajectory', 'Frame', 'x', 'y']]
    imdat = pickle.load(open(resultsfolder + exp_filename + '_segdata.pickle','rb'))


    labelmats = imdat['labels']
    n_frames = len(labelmats)

    print 'find full length track trajectories of %s' % exp_filename
    tsel = filterTrajectories(tdat, config['classification']['n_frames_min'])
    print 'assign new labels to %s' % exp_filename
    tsel = assignLabels(tsel, labelmats)
    tsel = removeTrajectoriesWithZeroLabel(tsel)
    print 'compute new labelmatrix for %s' % exp_filename
    labelvol = computeNewLabelVol(tsel, labelmats)
    
    # save new label volume 
    imdat['track_labelvol'] = labelvol 
    
    del imdat['labels']
    pickle.dump(imdat, open(resultsfolder + exp_filename + '_trackdata.pickle', 'wb'))


    exportOverlayImages(labelvol, resultsfolder, imagefolder, exp_filename)








