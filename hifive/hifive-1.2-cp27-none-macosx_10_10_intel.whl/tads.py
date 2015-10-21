#!/usr/bin/env python

"""
This is a module contains scripts for finding domains in HiC interaction data.

Concepts
--------

These functions rely on the :class:`HiC` class in conjunction with the :class:`Fend` and :class:`HiCData` classes.


API Documentation
-----------------
"""

import os
import sys

import numpy
import h5py
try:
    from mpi4py import MPI
except:
    pass

import libraries._hic_tads as _hic_tads
import hic_binning
import plotting

class TAD( object ):
    """
    """

    def __init__(self, hic):
        self.hic = hic

    def __getitem__(self, key):
        """Dictionary-like lookup."""
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            return None

    def __setitem__(self, key, value):
        """Dictionary-like value setting."""
        self.__dict__[key] = value
        return None

    def learn_TADs(self, maxsize=2000000, maxtreesize=25, p=3, q=12, gamma=0.5, chroms=[], binsize=10000,
                   minsize=50000):
        if isinstance(chroms, list) and len(chroms) == 0:
            chroms = list(self.hic.fends['chromosomes'][...])
        elif isinstance(chroms, str):
            chroms = [chroms]
        if maxsize % binsize != 0:
            print >> sys.stderr, ("Maximum TAD size must be a multiple of bin size.\n"),
            return
        self.parameters = {
            'maxsize': int(maxsize),
            'minsize': int(minsize),
            'maxtreesize': int(maxtreesize),
            'p': int(p),
            'q': int(q),
            'gamma': float(gamma),
            'binsize': int(binsize),
        }
        self.chromosomes = numpy.array(chroms)
        for chrom in chroms:
            self[chrom] = self.find_TAD(chrom)

    def find_TAD(self, chrom):
        p, q, gamma = self.parameters['p'], self.parameters['q'], self.parameters['gamma']
        maxdist = max(max(p, q) * self.parameters['binsize'], self.parameters['maxsize'])
        data = self.hic.cis_heatmap(chrom, binsize=self.parameters['binsize'], arraytype='compact',
                                    datatype='fend', include_diagonal=False, maxdistance=maxdist)
        #where = numpy.where(data[:, :, 0] == 0)
        #data[where[0], where[1], 1] = 0
        #where = numpy.where(data[:, :, 0] > 0)
        #data[where[0], where[1], 0] = numpy.log(data[where[0], where[1], 0] / data[where[0], where[1], 1])
        #data[where[0], where[1], 1] = 1
        maxbins = self.parameters['maxsize'] / self.parameters['binsize']
        minbins = self.parameters['minsize'] / self.parameters['binsize']
        n = data.shape[0]
        m = data.shape[1]
        print >> sys.stderr, ("\rFinding BI scores for chromosome %s...") % (chrom),
        BIs = numpy.zeros((n, m, 2), dtype=numpy.float32)
        BIs.fill(-numpy.inf)
        _hic_tads.find_BIs(data, BIs, p, minbins)
        where = numpy.where(BIs[:, :, 1] == 0)
        print numpy.amin(BIs[where[0], where[1], 0]), numpy.mean(BIs[where[0], where[1], 0]), numpy.amax(BIs[where[0], where[1], 0])        
        where = numpy.where(BIs[:, :, 1] == 1)
        print numpy.amin(BIs[where[0], where[1], 0]), numpy.mean(BIs[where[0], where[1], 0]), numpy.amax(BIs[where[0], where[1], 0])
        """
        BI_scores = numpy.zeros((n, maxbins - minbins + 1), dtype=numpy.float32)
        for i in range(minbins, maxbins + 1):
            BI_scores[:(n - i + 1), i - minbins] = BIs[:(n - i + 1), 0] * BIs[(i - 1):, 1]
        where = numpy.where(BI_scores <= 0.0)
        BI_scores[where] = -numpy.inf
        where = numpy.where(BI_scores > -numpy.inf)
        BI_scores[where] = BI_scores[where] ** gamma
        """
        where = numpy.where(data[:, :, 0] == 0)
        data[where[0], where[1], 1] = 0
        where = numpy.where(data[:, :, 0] > 0)
        data[where[0], where[1], 0] = numpy.log(data[where[0], where[1], 0] / data[where[0], where[1], 1])
        data[where[0], where[1], 1] = 1
        print >> sys.stderr, ("\rFinding TAD parameters for chromosome %s...") % (chrom),
        scores = numpy.zeros((n, maxbins + 1), numpy.float32)
        scores.fill(numpy.inf)
        std_params = numpy.zeros((n, maxbins + 1, 3), dtype=numpy.float32)
        _hic_tads.find_initial_TAD_std_params(data, BIs, scores, std_params, maxbins, minbins, gamma)
        """
        paths = numpy.zeros((n, maxbins - minbins + 2), dtype=numpy.int32)
        paths.fill(-1)
        path_scores = numpy.zeros((n + 1, maxbins - minbins + 2, 2), dtype=numpy.float32)
        #path_scores[:, :, 0].fill(numpy.inf)
        final_path = numpy.zeros(n, dtype=numpy.int32)
        _hic_tads.find_TAD_path(scores, paths, path_scores, final_path, minbins, maxbins)
        print list(final_path)
        for i in range(10):
            print list(path_scores[i, :, 0])
        where = numpy.where(numpy.abs(scores) < numpy.inf)
        print numpy.amin(scores[where]), numpy.mean(scores[where]), numpy.amax(scores[where])
        where = numpy.where(numpy.abs(BI_scores) < numpy.inf)
        print numpy.amin(BI_scores[where]), numpy.mean(BI_scores[where]), numpy.amax(BI_scores[where])
        """
        #numpy.savetxt('temp.txt',paths, fmt="%i", delimiter='\t')
        #subTAD_scores = numpy.zeros((n, maxbins - minbins + 1, self.parameters['maxtreesize']), dtype=numpy.float32)
        #subTAD_params = numpy.zeros((n, maxbins - minbins + 1, self.parameters['maxtreesize'], 3), dtype=numpy.float32)
        #_hic_tads.find_TAD_subparts(subTAD_scores, subTAD_params, BIs, std_params, minbins, gamma)
        #where = numpy.where(std_params[:, :, 0] >= 3)
        #errors = numpy.zeros((std_params.shape[0], std_params.shape[1], 2), dtype=numpy.float32)
        ##errors[where[0], where[1], 0] = (std_params[where[0], where[1], 2] / std_params[where[0], where[1], 0]) - (std_params[where[0], where[1], 1] / std_params[where[0], where[1], 0]) ** 2 - numpy.maximum(0, BIs[where[0], 0] * BIs[where[0] + where[1] + minbins - 1, 1])**gamma
        #print numpy.amax(where[0] + where[1] + minbins), BIs.shape
        #where1 = numpy.where(errors[where[0], where[1], 0] < 0)
        ##errors[where[0][where1], where[1][where1], 1] = 1
        #print numpy.mean(errors), numpy.amax(errors)
        #print numpy.amax(BIs), numpy.mean(BIs)
        #_hic_tads.find_betadeltas(data, betas, deltas, fits, errors, maxbins)
        #where = numpy.where(data[:, :, 0] == 0)
        #data[where[0], where[1], 1] = 0
        #where = numpy.where(data[:, :, 0] > 0)
        #data[where[0], where[1], 0] = numpy.log(data[where[0], where[1], 0] / data[where[0], where[1], 1])
        #data[where[0], where[1], 1] = 1
        """
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if BIs[i] < 0 or BIs[j] < 0:
                    fits[i,j] = numpy.inf
                else:
                    fits[i,j] -= gamma * (BIs[i] + BIs[j])
        print >> sys.stderr, ("\rFinding TAD trees for chromosome %s...") % (chrom),
        scores = numpy.zeros((n, n, self.parameters['maxtreesize']), dtype=numpy.float32)
        _hic_tads.build_TAD_trees(data, fits, deltas, betas, errors, scores, maxbins)
        """
        alldata = numpy.zeros((n, n, 2), dtype=numpy.float32)
        for i in range(data.shape[0] - 1):
            alldata[(i + 1):min(i + data.shape[1] + 1, n), i, :] = data[i, :min(data.shape[1], n - i - 1), :]
        for i in range(scores.shape[0] - 1 - minbins):
            where = numpy.where(numpy.abs(scores[i, :min(scores.shape[1], n - i - minbins - 1)]) < numpy.inf)[0]
            alldata[i, where + i + minbins, 0] = scores[i, where]
            alldata[i, where + i + minbins, 1] = 1
        """
        for i in range(BIs.shape[0] - 1):
            alldata[i, (i + 1):min(i + data.shape[1] + 1, n), :] = BIs[i, :min(data.shape[1], n - i - 1), :]
            #where = numpy.where(numpy.abs(BIs[i, :min(BIs.shape[1], n - i - 1), 1]) < numpy.inf)[0]
            #alldata[i, where + i, 0] = BIs[i, where, 1]
            #alldata[i, where + i, 1] = 1
        """
        indices = numpy.triu_indices(n, 1)
        where = numpy.where(alldata[indices[0], indices[1], 1] > 0)[0]
        alldata[indices[0][where], indices[1][where], 0] -= numpy.amin(alldata[indices[0][where], indices[1][where], 0])
        alldata[indices[0][where], indices[1][where], 0] /= numpy.amax(alldata[indices[0][where], indices[1][where], 0])
        where = numpy.where(alldata[indices[1], indices[0], 1] > 0)[0]
        alldata[indices[1][where], indices[0][where], 0] -= numpy.amin(alldata[indices[1][where], indices[0][where], 0])
        alldata[indices[1][where], indices[0][where], 0] /= numpy.amax(alldata[indices[1][where], indices[0][where], 0])
        """
        for i in range(n):
            if final_path[i] != 0:
                indices = numpy.triu_indices(final_path[i], 1)
                temp = alldata[i + final_path[i] - 1, i, 0]
                alldata[indices[1] + i, indices[0] + i, :] = 1.0
                alldata[i + final_path[i] - 1, i, 0] = temp
        """
        img = plotting.plot_full_array(alldata, symmetricscaling=False, logged=False)
        img.save('BIs_%s.png' % chrom)











