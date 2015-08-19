import logging

from stashcache_tester.output.generalOuput import GeneralOutput
import numpy
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt

from stashcache_tester.util.Configuration import get_option

class MatplotlibOutput(GeneralOutput):
    def __init__(self, sitesData):
        GeneralOutput.__init__(self, sitesData)
        
        
    def startProcessing(self):
        logging.debug("Starting processing with matplotlib...")
        
        # Lines for download times
        for site in self.sitesData:
            siteTimes = self.sitesData[site]
            list_downloads = sorted(siteTimes, key=lambda k: k['starttime'])
            
            for run in range(len(list_downloads)):
                cur = list_downloads[run]
                plt.plot([cur['starttime'], cur['endtime']], [(run*2)+1, (run*2)+1])
            
            plt.ylabel("Run Number")
            plt.xlabel("Time since unix Epoch")
            plt.savefig("%s_downloads.png" % site)
            plt.clf()
            
        # Make a violin plot
        downloadTimes = {}
        for site in self.sitesData:
            siteTimes = self.sitesData[site]
            
            downloadTimes[site] = []
            
            for time in siteTimes:
                downloadTimes[site].append(float(time['endtime']) - float(time['starttime']))
            
            testsize = get_option("raw_testsize")
            downloadTimes[site] = (float(testsize*8) / (1024*1024)) / numpy.array(downloadTimes[site])
            
            
        plt.violinplot(downloadTimes.values())
        plt.xticks(range(1, len(downloadTimes.keys())+1), downloadTimes.keys())
        plt.ylabel("Mb per second")
        plt.xlabel("Site")
        plt.savefig("violinplot.png")
        plt.clf()
            
        
        
        
        
        
