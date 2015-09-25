"""D9C2 scoring function



"""
from dreamtools import Challenge


class D9C2(Challenge):
    """A class dedicated to D9C2 challenge

    ::

        from dreamtools import D9C2
        s = D9C2()
        filename = s.download_template() 
        s.score(filename) 

    Data and templates are downloaded from Synapse. You must have a login.

    """
    def __init__(self):
        """.. rubric:: constructor

        """
        super(D9C2, self).__init__('D9C2')
        self.sub_challenges = ['sc1', 'sc2', 'sc3']
        print("GS not yet released (aug 2015)")

    def score(self, filename, subname=None, goldstandard=None):
        raise NotImplementedError

    def download_template(self, subname=None):
        # should return full path to a template file
        self._check_subname(subname)
        if subname == 'sc1':
            filename = self.getpath_template('template_100_Q1.csv')
        elif subname == 'sc2':
            filename = self.getpath_template('template_100_Q2.csv')
        elif subname == 'sc3':
            filename = self.getpath_template('template_100_Q3.csv')
        return filename

    def download_goldstandard(self, subname=None):
        # should return full path to a gold standard file
        raise NotImplementedError
