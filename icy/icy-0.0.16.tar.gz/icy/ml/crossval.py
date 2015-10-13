import pandas as pd
import numpy as np
from sklearn.cross_validation import KFold
import xgboost as xgb
from datetime import datetime
from copy import deepcopy

class KLabelFolds():
    def __init__(self, labels, n_folds=3):
        self.labels = labels
        self.n_folds = n_folds

    def __iter__(self):
        try:
            unique_labels = self.labels.unique()
        except:
            unique_labels = np.unique(self.labels)
        cv = KFold(len(unique_labels), self.n_folds)
        for train, test in cv:
            test_labels = unique_labels[test]
            try:
                test_mask = self.labels.isin(test_labels)
            except:
                test_mask = np.in1d(self.labels, test_labels)
            train_mask = np.logical_not(test_mask)
            yield (np.where(train_mask)[0], np.where(test_mask)[0])
    
    def __len__(self):
        return self.n_folds

def ensemble_cv(lst, data, labels, scoring=None, cv=None, test=None):
    try:
        if round(sum([e[0] for e in lst]), 3) == 1.0:
            weights = True
        else:
            weights = False
            print('WARNING: weights dont add up to 100%, using equal weights')
    except:
        weights = None
    
    if type(cv) != type(None):
        print('model ensemble crossval ...')
        scores = []
        counter = 1
        t0 = datetime.now()
        for train_ix, test_ix in cv:
            t1 = datetime.now()
            y_pred = []
            X_train, y_train = data.loc[train_ix, :], labels.loc[train_ix]
            X_test, y_test = data.loc[test_ix, :], labels.loc[test_ix]
            
            for elem in lst:
                if weights == True:
                    weight, model = elem
                elif weights == False:
                    weight, model = 1/len(lst), elem[1]
                elif weights == None:
                    weight, model = 1/len(lst), elem
                model.fit(X_train, y_train)
                y_pred.append(model.predict(X_test) * weight)

            y_pred = pd.concat([pd.Series(i) for i in y_pred], axis=1).sum(axis=1)
            try:
                score = scoring._score_func(y_test, y_pred)
            except AttributeError:
                score = scoring(y_test, y_pred)
            scores.append(score)
            print('Job: {}/{} - Score: {:.4f} - Runtime last: {:.1f} min, total: {:.1f} min'.format(counter, len(cv), score, (datetime.now()-t1).total_seconds()/60, (datetime.now()-t0).total_seconds()/60))
            counter += 1
        return np.array(scores)
    elif type(test) != type(None):
        t0 = datetime.now()
        counter = 1
        print('model ensemble prediction ...')
        preds = []
        for elem in lst:
            t1 = datetime.now()
            if weights == True:
                weight, model = elem
            elif weights == False:
                weight, model = 1/len(lst), elem[1]
            elif weights == None:
                weight, model = 1/len(lst), elem
            model.fit(data, labels)
            preds.append(model.predict(test) * weight)
            print('Job: {} of {} - Runtime last: {:.1f} min, total: {:.1f} min'.format(counter, len(lst), (datetime.now()-t1).total_seconds()/60, (datetime.now()-t0).total_seconds()/60))
            counter += 1
        return pd.concat([pd.Series(i).astype(float) for i in preds], axis=1).sum(axis=1)
    else:
        raise AttributeError('specify either cv or test to run ensemble_cv')
