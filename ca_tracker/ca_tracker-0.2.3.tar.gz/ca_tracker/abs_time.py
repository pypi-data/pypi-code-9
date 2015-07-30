
import ca_tracker.idaf_io as iio
import pandas as pd
import numpy as np
import os



def getFramesPerModule(times):
    '''
    get a list of frame lists where each framelist corresponds to one module module 
    input the labelvolume and the timetlable
    '''
    #frames_labelvol = range(labelvol.shape[0])
    frames_ca = range(times.frame_nr.count())
    mod_nr  = times.filename.apply(lambda name: int(name[0])).tolist()

    switch_frames = [-1] + list(np.nonzero(np.diff(np.array(mod_nr)))[0]) + [frames_ca[-1]]# at these frames the imaging mode is switched

    frames = []
    for i in range(len(switch_frames)-1):
        frames.append(range(switch_frames[i]+1, switch_frames[i+1]+1)) 
    return frames   

def count_up_nested(lstlst):
    counter = 0
    for i in range(len(lstlst)):
        for j in range(len(lstlst[i])):
            lstlst[i][j] = counter
            counter += 1
    return lstlst       


def getFramesToSp(frames_per_mod):
    ca_mod_index = range(len(frames_per_mod))[::2] # index of calcium modules
    sp_mod_index = [e+1 for e in ca_mod_index] # index of calcium modules

    #nested lists, eahc list is one module
    frames_per_mod_ca = [frames_per_mod[i] for i in ca_mod_index]
    frames_per_mod_sp = [frames_per_mod[i] for i in sp_mod_index]
    frames_per_mod_sp = count_up_nested(frames_per_mod_sp)

    ca_mod_nrs = [e+1 for e in ca_mod_index] #list of module numbers of type ca
    sp_mod_nrs = [e+1 for e in sp_mod_index] # list of module numbers of type sp

    #frames_labelvol = range(labelvol.shape[0])
    #frames_ca = range(times.frame_nr.count())
    #mod_nr  = times.filename.apply(lambda name: int(name[0])).tolist()


    frames_to_sp = []
    for i in range(len(frames_per_mod_sp)):
        for j in range(len(frames_per_mod_ca[i])+1):
            frames_to_sp.append(frames_per_mod_sp[i][0])

    frames_to_sp =  frames_to_sp + frames_per_mod_sp[-1][1:] # add last timeseries(specking)        
    return frames_to_sp





def compute_time_inner(row, dt_ca, dt_sp):
    if row['module_type'] == 'ca':
        
        out = row['frame_nr'] * dt_ca
    if row['module_type'] == 'sp':
        out = row['frame_nr'] * dt_sp   
    return out  


def compute_timetable(filenames, dt_ca, dt_sp):
    #init table
    dat = pd.DataFrame(columns=['filename', 'module_nr', 'module_type', 'frame_nr', 'frames_to_sp', 'time'])

    #remove channel info from filenames
    filenames_short = []
    for filename in filenames:
        filenames_short.append(filename[:-9])
    filenames_short = np.unique(filenames_short)    
    filenames_short.sort()

    #add location information (extratced from filenames)
    for filename in filenames_short:
        row = {}
        
        row['filename'] = filename
        row['module_nr'] = int(filename[0])
        row['module_type'] = filename[2:4]
        row['frame_nr'] = int(filename[6:])-1
        dat = dat.append(row, ignore_index=True)

    
    #frames of sp modules transferrred to ca frames
    frames_per_mod = getFramesPerModule(dat)
    dat['frames_to_sp'] = getFramesToSp(frames_per_mod) 

    #add time in seconds for each module
    dat['time'] = dat.apply(lambda row: compute_time_inner(row, dt_ca, dt_sp), axis=1) 

    # calculate absolute time in seconds
    endtimes = dat.groupby(dat['module_nr'])['time'].max()
    types = dat.groupby(dat['module_nr'])['module_type'].max()
    timer = 0
    time_abs = []
    grouped = dat.groupby('module_nr')
    for name, group in grouped:
        time_abs_group =  group['time'] + timer
        time_abs = time_abs + time_abs_group.tolist()
        timer = time_abs[-1] + dt_ca
    dat['time_abs'] = time_abs

    return dat  







def abs_time(exp_filename, config):

    pattern = '.tif'
    path = config.imagefolder + exp_filename + '_singlechannel'

    #all image filenames
    filenames = iio.getFilelistFromDir(path,pattern)
    timetable = compute_timetable(filenames, config.dt_ca, config.dt_sp)
    timetable.to_csv(config.resultsfolder + exp_filename + '_timetable.csv')





