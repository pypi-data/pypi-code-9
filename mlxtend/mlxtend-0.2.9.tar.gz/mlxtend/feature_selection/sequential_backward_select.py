# Sebastian Raschka, 2015
# Function for sequential feature selection via
# Sequential Backward Selection (SBS)
# mlxtend Machine Learning Library Extensions

from sklearn.base import clone
from sklearn.base import BaseEstimator
from sklearn.base import MetaEstimatorMixin
from itertools import combinations
from sklearn.cross_validation import cross_val_score
import numpy as np
import sys


class SBS(BaseEstimator, MetaEstimatorMixin):
    """ Sequential Backward Selection for feature selection.

    Parameters
    ----------
    estimator : scikit-learn estimator object

    k_features : int
      Number of features to select where k_features.

    print_progress : bool (default: True)
       Prints progress as the number of epochs
       to stderr.

    scoring : str, (default='accuracy')
      Scoring metric for the cross validation scorer.

    cv : int (default: 5)
      Number of folds in StratifiedKFold.

    n_jobs : int (default: 1)
      The number of CPUs to use for cross validation. -1 means 'all CPUs'.

    Attributes
    ----------
    indices_ : array-like, shape = [n_predictions]
      Indices of the selected subsets.

    k_score_ : float
      Cross validation mean score of the selected subset

    subsets_ : list of lists
      Indices of the sequentially selected subsets.

    scores_ : list
      Cross validation mean scores of the sequentially selected subsets.

    Examples
    --------
    >>> from sklearn.neighbors import KNeighborsClassifier
    >>> from sklearn.datasets import load_iris
    >>> iris = load_iris()
    >>> X = iris.data
    >>> y = iris.target
    >>> knn = KNeighborsClassifier(n_neighbors=4)
    >>> sbs = SBS(knn, k_features=2, scoring='accuracy', cv=5)
    >>> sbs = sbs.fit(X, y)
    >>> sbs.indices_
    (0, 3)
    >>> sbs.transform(X[:5])
    array([[ 5.1,  0.2],
           [ 4.9,  0.2],
           [ 4.7,  0.2],
           [ 4.6,  0.2],
           [ 5. ,  0.2]])

    >>> print('best score: %.2f' % sbs.k_score_)
    best score: 0.96

    """
    def __init__(self, estimator, k_features, print_progress=True,
                 scoring='accuracy', cv=5, n_jobs=1):
        self.scoring = scoring
        self.estimator = estimator#clone(estimator)
        self.cv = cv
        self.k_features = k_features
        self.print_progress = print_progress
        self.n_jobs = n_jobs

    def fit(self, X, y):

        dim = X.shape[1]
        self.indices_ = tuple(range(dim))
        self.subsets_ = [self.indices_]
        cv_score = self._calc_score(X, y, self.indices_)
        self.scores_ = [cv_score.mean()]

        while dim > self.k_features:
            scores = []
            subsets = []

            for p in combinations(self.indices_, r=dim-1):
                cv_score = self._calc_score(X, y, p)
                scores.append(cv_score.mean())
                subsets.append(p)

            best = np.argmax(scores)
            self.indices_ = subsets[best]
            self.subsets_.append(self.indices_)
            dim -= 1

            self.scores_.append(scores[best])

            if self.print_progress:
                sys.stderr.write('\rFeatures: %d/%d' % (len(self.indices_), self.k_features))
                sys.stderr.flush()

        self.k_score_ = self.scores_[-1]

        return self

    def transform(self, X):
        return X[:, self.indices_]

    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)

    def _calc_score(self, X, y, indices):
        cv_score = cross_val_score(self.estimator,
                                   X[:, indices], y,
                                   cv=self.cv,
                                   scoring=self.scoring,
                                   n_jobs=self.n_jobs)
        return cv_score
