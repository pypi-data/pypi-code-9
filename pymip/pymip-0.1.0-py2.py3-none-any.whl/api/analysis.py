# -*- coding: utf-8 -*-
from __future__ import division

from path import path
import yaml

from pymip.compat import iteritems


class FamilyOutput(object):

    """docstring for FamilyOutput"""

    def __init__(self, base_path, load=False):
        super(FamilyOutput, self).__init__()
        self.base_path = path(base_path)
        self.family_id = None
        self._data = None
        self.samples = []

        if load:
            self.load()

    def load(self):
        """Load an analysis family into the class object."""
        # extract the name of the family directory
        family_id = self.base_path.basename()
        self.family_id = int(family_id) if family_id.isdigit() else family_id

        # read in the YAML QC metrics file
        files = [file_path for file_path in self.base_path.listdir()
                 if file_path.endswith('_qcmetrics.yaml')]

        try:
            qc_file = files[0]
        except IndexError:
            # QC metrics file didn't exist as expected
            raise IOError("QC metrics file not found: {}"
                          .format(self.base_path))

        # open and read the (existing) QC metrics file
        with qc_file.open() as handle:
            data = yaml.load(handle).values()[0]

        # do some initial parsing to lose superfulous data
        for key, values in iteritems(data):
            if key == self.family_id:
                # store QC data subtree
                self._data = values

            else:
                # add a sample output instance
                self.samples.append(SampleOutput(key, data=values))


class SampleOutput(object):

    """docstring for SampleOutput"""

    def __init__(self, sample_id, data=None):
        super(SampleOutput, self).__init__()
        self.sample_id = sample_id
        self._raw = data

        # store the subtree with actually relevant data ("all lanes")
        for key, value in iteritems(data):
            if 'lanes' in key:
                self._data = value

    @property
    def total_reads(self):
        """Return the total number of reads."""
        return (self._data['CalculateHsMetrics']['Header']['Data']
                          ['TOTAL_READS'])

    @property
    def total_reads_m(self):
        """Return the total number of reads."""
        return self.total_reads / 1000000

    @property
    def duplicates(self):
        """Return the duplicates in percent."""
        return (self._data['MarkDuplicates']['Header']['Data']
                          ['PERCENT_DUPLICATION'])

    @property
    def mean_target_coverage(self):
        """Return mean target coverage."""
        return (self._data['CalculateHsMetrics']['Header']['Data']
                          ['MEAN_TARGET_COVERAGE'])

    @property
    def off_bait(self):
        """Return off bait in percent."""
        return (self._data['CalculateHsMetrics']['Header']['Data']
                          ['PCT_OFF_BAIT'])

    @property
    def aligned_reads(self):
        """Return the pass filter unique align reads."""
        count = (self._data['CalculateHsMetrics']['Header']['Data']
                           ['PF_UQ_READS_ALIGNED'])
        return count / self.total_reads

    @property
    def ti_tv(self):
        """Return Ti/Tv ratio."""
        return (self._data['CalculateHsMetrics']['Header']['Data']
                           ['PF_UQ_READS_ALIGNED'])

    @property
    def gender(self):
        """Return the predicted gender by chanjo."""
        return self._data['ChanjoSexCheck']['gender']

    def target_coverage(self, level=10):
        """Return target coverage at different levels."""
        return (self._data['CalculateHsMetrics']['Header']['Data']
                          ["PCT_TARGET_BASES_{}X".format(level)])

