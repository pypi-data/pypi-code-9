
"""D9C4 scoring function


Requires pysam from pypi
and pyvcf from Requires PyVCF (https://github.com/jamescasbon/PyVCF)


download data:

https://www.synapse.org/#!Synapse:syn2280639

sage/github code: 

https://github.com/Sage-Bionetworks/ICGC-TCGA-DREAM-Mutation-Calling-challenge-tools

https://www.synapse.org/#!Synapse:syn312572/wiki/

"""
import os
from dreamtools.core.challenge import Challenge


class D9C4(Challenge):
    """A class dedicated to D9C4 challenge


    ::

        from dreamtools import D9C4
        s = D9C4()
        filename = s.download_template() 
        s.score(filename) 

    Data and templates are downloaded from Synapse. You must have a login.

    """
    def __init__(self):
        """.. rubric:: constructor

        """
        super(D9C4, self).__init__('D9C4')
        self._init()
        self.sub_challenges = []

    def _init(self):
        # should download files from synapse if required.
        pass

    def score(self, filename, subname=None, goldstandard=None):
        raise NotImplementedError

    def download_template(self, subname=None):
        # should return full path to a template file
        raise NotImplementedError

    def download_goldstandard(self, subname=None):
        # should return full path to a gold standard file
        raise NotImplementedError
