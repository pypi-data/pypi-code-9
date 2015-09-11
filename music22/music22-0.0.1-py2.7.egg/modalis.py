# -*- coding: utf-8 -*-
"""
Modalis: Basics of Modality
===========================

The module **modalis** focuses on the fundamental elements of modality in a melody. Its defines a Melodie class for getting :

* The Dominant : It is based on :
    ** The most present frequency (Todo).
    ** The most probable frequency.

"""

import os, glob, time, numpy
import matplotlib.pyplot as plt

from music22 import core, diastema, scale, audio, stats

class melodies(object):
    """This class defines a set of `melodia`-a and compares them.
    
    """
    def __init__(self,path):

        self.path = path
        print "Reading the content of :", self.path
        print '\n'
                
        # Information about files in path
        print "Audios files are :"
        self.wavfiles = glob.glob(self.path+'*.wav')
        
        self.melodies = []
        self.labels = []
        
        for file in self.wavfiles:
            self.melodies.append(melodia(file))
            print file,'appended'
            self.labels.append(melodia(file).name)
        print '\n'
        ##
            
    def pdf_show(self,width=12,height=6):
        plt.figure(figsize=(width,height))
        for i in range(0,len(self.melodies)):
            self.melodies[i].pdf_show()
            
    def corr(self,metric='KL'):
        """Calculate distances between PDFs.
        
        Args:
            self.melodies.pdf (list) : list of pdf lists.
            metric (str) : the metric method : euclidian, KL (Kullback-Leibler). Default is KL.
        Return:
            self.distances
        """
        PDFS = []
        for i in range(0,len(self.melodies)):
            PDFS.append(self.melodies[i].pdf)

        self.distances = stats.corr(PDFS,metric)
        return
        
    def matrix(self):
        """Plot the matrix and heatmap of PDFS."""
        try:
            stats.matrix(self.distances,self.labels)
        except AttributeError:
            self.corr(metric='KL')
            stats.matrix(self.distances,self.labels)        
        return
        
class melodia(object):
    def __init__(self,file_path):
        """Create the melodia object.
        
        Args:
            A path to a list of frequencies (f0) in a .txt file.
        
        Attributes:
            All attributes from music22.core.f0file.
            clean_freqs (numpy.ndarray): The list of frequencies without Zeros neither NaNs.
            pdf (numpy.ndarray): The Probability Density Function on the range 0-500 Hz.
            xpeaks, xpeaks (numpy.ndarray): the Peaks of the PDF and their values.
            ordredpeaks (pandas.core.frame.DataFrame): The Peaks ordered by their probability.
            dominante (numpy.float64): the dominant frequency.
            intervals (pandas.core.series.Series): the list of intervals in the choosen Unit (default is `savarts`).
            scale (list): the Scale from the Dominant, compared to reference epimoric intervals.
            pdf_show (matplotlibfigure): the PDF plot with peaks.
        
        Example:
            >>> import music22.modalis
            >>> file = '/Users/anas/AUDIO/Barraq/P1.wav'
            >>> Barraq = music22.modalis.melodia(file)
            Instance created with the txt file : P1.wav
            Instance created with the txt file : P1.txt
            The detected tonic is 167.696 Hz.
            >>> Barraq.file.basename
            'P1.txt'
            >>> Barraq.freqs
            array([ nan,  nan,  nan, ...,  nan,  nan,  nan])
            >>> Barraq.clean_freqs
            array([ 155.564,  157.372,  160.123, ...,  159.201,  158.284,  156.466])
            >>> Barraq.tonique
            167.696
            >>> Barraq.pdf
            array([  1.55304474e-33,   5.65209492e-33,   2.03065388e-32,
                     7.20217980e-32,   2.52170476e-31,   8.71620406e-31,
                     [...]
                     8.53621504e-26,   2.80105445e-26,   9.07308675e-27,
                     2.90111852e-27,   9.15698236e-28])
            >>> Barraq.pdf_show
            <bound method melodia.pdf_show of <music22.modalis.melodia object at 0x102a32910>>
            >>> Barraq.ordredpeaks
                   xpeaks    ypeaks
            1  243.486974  0.012244
            0  201.402806  0.007772
            3  324.649299  0.003007
            2  278.557114  0.002709
            4  375.751503  0.000785
        """
        file = core.file(file_path)
        if file.extension == 'wav':
            self.file = core.wavfile(file_path)
            txt_file = self.file.dirname+'/f0/'+self.file.name+'.txt'
            if not os.path.isfile(txt_file):
                self.file.pitch_extract()
            self.file = core.f0file(txt_file)
        elif file.extension == 'txt':
            self.file = core.f0file(file_path)
        
        self.name = self.file.name
        self.file.get_data()
        self.file.clean_data()
        self.freqs = self.file.data
        self.clean_freqs = self.file.clean_data
        
        self.xmin = numpy.min(self.clean_freqs)
        self.xmax = numpy.max(self.clean_freqs)
        
        self.get_tonique()
        
        self.pdf = scale.kde(self.clean_freqs)
        self.xpeaks, self.ypeaks = scale.peaks(self.pdf)
        self.ordredpeaks = scale.order_peaks(self.xpeaks,self.ypeaks)
        self.dominante = self.ordredpeaks['xpeaks'].iloc[0]
        
        
    def get_scale(self,reference="tonic"):
        """Get the scale of the melody.
        
        Args:
            reference (float): the reference frequencies to calculate the scale. It could be the _tonic_ (self.tonique) or the _domin_ (self.dominante)
        Return:
            self.intervals (list) : the intervals in the the choosen linear Unit.
            self.scale (): The scale compared to reference intervals.
        """
        if reference == 'tonic':
            print 'reference is tonic'
            self.intervals = diastema.dias(self.ordredpeaks['xpeaks']/self.tonique)
            print self.intervals
        if reference == 'domin':
            print 'reference is dominant'
            self.intervals = diastema.dias(self.ordredpeaks['xpeaks']/self.dominante)
            print self.intervals

        scale = []
        x = 0
        for interval in self.intervals:
            var = (self.ordredpeaks['xpeaks'].iloc[x].astype('str'), diastema.get_inter_ref(interval))
            scale.append(var)
            x = x + 1
        self.scale = scale

    def plot(self,peaks="Yes",width=12,height=6):
        """
        Plots the melody frequencies
    
        Args:
            peaks (boolean, optional) : Draw the peak-lines. Default="Yes"
            width (int,optional) : width of the figure. Default = 12
            height (int,optional) : height of the figure. Default = 6
        """
        hopSize = 128
        frameSize = 2048
        sampleRate = 44100
    
        n_frames = len(self.freqs)
        
        fig = plt.figure(figsize=(width,height))
        plt.plot(range(n_frames), self.freqs, 'bo')
        n_ticks = 10
        xtick_locs = [i * (n_frames / 10.0) for i in range(n_ticks)]
        xtick_lbls = [i * (n_frames / 10.0) * hopSize / sampleRate for i in range(n_ticks)]
        xtick_lbls = ["%.2f" % round(x,2) for x in xtick_lbls]
        plt.xticks(xtick_locs, xtick_lbls)
        
        ax = fig.add_subplot(111)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Pitch (Hz)')
        plt.suptitle(self.name)
        
        if peaks=="Yes" :
            plt.yticks(self.ordredpeaks['xpeaks'].tolist())
            c = ['r','g','y','b','b','b','b','b','b','b','b','b']
            for i in range(0,len(self.ordredpeaks)):
                l = plt.axhline(y=self.ordredpeaks['xpeaks'].tolist()[i],color=c[i])
                plt.text(len(self.freqs), self.ordredpeaks['xpeaks'].tolist()[i], self.scale[i][1])
        elif peaks=="No" :
            pass
        
    def pdf_show(self):
        """Show the pdf."""
        scale.pdf_show(self.pdf,self.xpeaks,self.ypeaks,label=self.name)

    def get_tonique(self,percent=0.5,method="pdf"):
        """Get the tonic of a melody.
        
        Args:
            percent (float): the percentage of the last considered frequencies.
            method (str): The method to be used for the analysis : "pdf" or "mode".
        Return:
            tonic (float): The detected tonic.
        """
        print "coucou",method
        self.percent = percent
        self.method = method
        
        L = len(self.clean_freqs)
        Nb_Frames = L*self.percent/100
        Final_Freqs = self.clean_freqs[(L-Nb_Frames):L]
        self.final_freqs = Final_Freqs
        
        if method=='mode':
            self.tonique = self._tonique_mode(Final_Freqs)
        elif method=='pdf':
            self.tonique = self._tonique_pdf(Final_Freqs)
        
        print 'The detected tonic is', self.tonique, 'Hz.'
        
    #def _tonique_mode(Final_Freqs):
        #from scipy.stats.mstats import mode

    def _tonique_pdf(self,Final_Freqs):
        from scipy.stats.kde import gaussian_kde
    
        final_pdf = gaussian_kde(Final_Freqs)
        xmin_range = numpy.min(Final_Freqs)
        xmax_range = numpy.max(Final_Freqs)
        y = numpy.arange(xmin_range,xmax_range)
        lmax = Final_Freqs[numpy.argmax(final_pdf(y))]
        return float(lmax)


if __name__ == "__main__":
    import doctest
    doctest.testmod()