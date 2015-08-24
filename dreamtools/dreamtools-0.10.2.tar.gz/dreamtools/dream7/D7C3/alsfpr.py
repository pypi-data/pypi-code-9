import pandas as pd
from easydev import Progress
import numpy as np

class ALSFRS(object):

    """Data obtained from PROACT website

    The time between the first time a patient was observed (Time 0) and the time
    of each assessment of ALSFRS or ALSFRS-R over the course of the trial is
    listed as [ALSFRS-Delta (regardless of whether it was ALSFRS or ALSFRS-R)]. 
    """
    def __init__(self):

        self.df = pd.read_csv("/home/cokelaer/PROACT_ALSFRS.csv")
        self.teams = pd.read_csv('data/solvers_predictions/team3.predicted.out',
            header=None)[0].values




    def get_slopes(self):
        # ALSFRS Total contains 10 questions
        # ALSFRS-R Total contains 12 questions
        # some entries do not have ALSFRS, in which case ALSFRS-R is taken
        # minus the 2 extra questyions (Dyspnea and Orthopnea)

        self.df['ALSFRS-R Total'] -= self.df[[u'R-1. Dyspnea', u'R-2. Orthopnea']].sum(axis=1)


        groups = self.df.groupby('SubjectID').groups
        self.slopes = {}
        self.slopes1 = {}
        self.slopes2 = {}
        self.firstmonth = {}
        self.lastmonth = {}
        pb = Progress(len(groups))
        for i, subject in enumerate(groups.keys()):
            if subject not in self.teams:
                continue

            subdf = self.df.ix[groups[subject]][['ALSFRS Total', 
                'ALSFRS Delta', 'ALSFRS-R Total']]
            subdf.fillna(method='pad', inplace=True)

            # filter data that are below month 3
            subdf = subdf[subdf['ALSFRS Delta'] >= 90]
            subdf = subdf[subdf['ALSFRS Delta'] <= 365]
            if len(subdf) == 0:
                continue

            #print subject, subdf
            dY1 = (subdf['ALSFRS Total'].values[-1] - 
                    subdf['ALSFRS Total'].values[0])
            dY2 = (subdf['ALSFRS-R Total'].values[-1] - 
                    subdf['ALSFRS-R Total'].values[0])
            # Either dY1 is NA or dY2 is NA but not both at the same time
            dY = np.nansum([dY1, dY2])

            self.firstmonth[subject] = subdf['ALSFRS Delta'].values[0]
            self.lastmonth[subject] = subdf['ALSFRS Delta'].values[-1]

            dX = (subdf['ALSFRS Delta'].values[-1] - 
                    subdf['ALSFRS Delta'].values[0])
            self.slopes1[subject] = dY1/float(dX)
            self.slopes2[subject] = dY2/float(dX)
            self.slopes[subject] = dY / float(dX)

            pb.animate(i+1)

        return self.slopes

