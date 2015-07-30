import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
def plot_graphs(dat, savepath=None):
    cv = []
    un = []
    plt.close()
    fig, ax = plt.subplots(2,1)
    #plotTsClasses(dat,ax[0], 'is_specking'\
    #    , 'cv_s', xlabel=False, ylabel='cv contrast asc channel')
    #ax[0].set_ylim([0, 1])
    plotTsClasses(dat,ax[0], 'is_specking'\
        , 'rel_max_s', xlabel=True, ylabel='spot_probability')

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



def plotTsClasses(dat,ax, filter_col, feature, xlabel=False, ylabel=None):
    y_agg, time = getPlottingDataByClassname(dat,filter_col, feature)
    y_hom, time = getPlottingDataByClassname(dat,filter_col, feature, yesno = False)
    time = time/60 #time in minutes
    if len(y_agg)>0:
        sns.tsplot(y_agg, time=time, err_style="unit_traces", color = 'r', ax = ax) 
    if len(y_hom)>0:
        sns.tsplot(y_hom, time=time, err_style="unit_traces", color = 'b', ax = ax)         
    if xlabel:
        ax.set_xlabel('time [min]')
    if ylabel is not None:
        ax.set_ylabel(ylabel)    



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


def tableToList(dat):
    return [dat[key].tolist() for key in dat.columns]


def plotLongSeries(ax,hom,sp,times,y_hom,y_agg,time, err_style='ci_band', xlim = None):
    sns.tsplot(hom, time=times.time_abs, color = 'b', ax=ax[0], err_style=err_style, estimator=np.nanmean) 
    sns.tsplot(sp, time=times.time_abs, color = 'r', ax=ax[0], err_style=err_style, estimator=np.nanmean)

    sns.tsplot(y_hom, time=time, color = 'b', ax=ax[1], err_style=err_style, estimator=np.nanmean) 
    sns.tsplot(y_agg, time=time, color = 'r', ax=ax[1], err_style=err_style, estimator=np.nanmean)
    if xlim is not None:
        ax[0].set_xlim(xlim)
        ax[1].set_xlim(xlim)

    ax[1].set_xlabel('time [s]')
    ax[1].set_ylabel('specking_measure')
    ax[0].set_xlabel('')
    ax[0].set_ylabel('abs ca intensity')


def plotCaSeries(ax,hom,sp,times,time, xlim = None):
    sns.tsplot(hom, time=times.time_abs, color = 'b', ax=ax[0], err_style='unit_traces', estimator=np.nanmean) 
    sns.tsplot(sp, time=times.time_abs, color = 'r', ax=ax[0], err_style='unit_traces', estimator=np.nanmean)

    sns.tsplot(hom, time=times.time_abs, color = 'b', ax=ax[1], err_style='ci_band', estimator=np.nanmean) 
    sns.tsplot(sp, time=times.time_abs, color = 'r', ax=ax[1], err_style='ci_band', estimator=np.nanmean)

    if xlim is not None:
        ax[0].set_xlim(xlim)
        ax[1].set_xlim(xlim)

    ax[1].set_xlabel('time [s]')
    ax[1].set_ylabel('abs ca intensity')
    ax[0].set_xlabel('')
    ax[0].set_ylabel('abs ca intensity')


    
def plot_profiles(exp_filename, config):

    resultsfolder = config['data_locations']['resultsfolder']
    imagefolder = config['data_locations']['imagefolder']

    times = pd.read_csv(resultsfolder + exp_filename + '_timetable.csv')
    dat_speck = pd.read_csv(resultsfolder + exp_filename + '_intensities_speck.csv')
    dat_hom = pd.read_csv(resultsfolder + exp_filename + '_intensities_hom.csv')

    dat_classes = pd.read_csv(resultsfolder + exp_filename + '_classes.csv')
    dat_features = pd.read_csv(resultsfolder + exp_filename + '_features.csv')
    dat_features_classes = pd.merge(dat_features,dat_classes, on=['label'])

    dat_speck.pop(dat_speck.columns[0])
    dat_hom.pop(dat_hom.columns[0])

    #ca data
    sp = tableToList(dat_speck)
    hom = tableToList(dat_hom)
    #speck data
    y_agg, time = getPlottingDataByClassname(dat_features_classes,'is_specking', 'rel_max_s')
    y_hom, time = getPlottingDataByClassname(dat_features_classes,'is_specking', 'rel_max_s', yesno = False)


    plt.close()
    fig, ax = plt.subplots(2,1)
    fig2, ax2 = plt.subplots(2,1)
    fig3, ax3 = plt.subplots(2,1)

    time_ca_max = times[times.module_nr == times.module_nr.max()].time_abs.values[0]

    plotLongSeries(ax,hom,sp,times,y_hom,y_agg,time, err_style='ci_band') # whole timeseries 
    plotLongSeries(ax2,hom,sp,times,y_hom,y_agg,time, err_style='unit_traces') #whole timeseries mean and std
    plotCaSeries(ax3,hom,sp,times,time, xlim = [0,time_ca_max]) #only high time resolution plots

    savefolder = resultsfolder + exp_filename + '_plots/' 
    fig.savefig(savefolder + exp_filename + '_ca_specking_mean.pdf')
    fig2.savefig(savefolder + exp_filename + '_ca_specking_single.pdf')
    fig3.savefig(savefolder + exp_filename + '_ca_only.pdf')

    #dat_hom.plot()






