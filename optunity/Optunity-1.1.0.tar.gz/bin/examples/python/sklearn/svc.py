# Example of tuning an SVC model in scikit-learn with Optunity
# This example requires sklearn

import optunity
import optunity.metrics
import sklearn.svm
import numpy
import time

# CREATE THE TRAINING SET
from sklearn.datasets import load_digits
digits = load_digits()
n = digits.data.shape[0]

positive_digit = 8
negative_digit = 9

positive_idx = [i for i in range(n) if digits.target[i] == positive_digit]
negative_idx = [i for i in range(n) if digits.target[i] == negative_digit]

# add some noise to the data to make it a little challenging
original_data = digits.data[positive_idx + negative_idx, ...]
data = original_data + 5 * numpy.random.randn(original_data.shape[0], original_data.shape[1])
labels = [True] * len(positive_idx) + [False] * len(negative_idx)

# we will use nested 3-fold cross-validation
# in the outer cross-validation procedure
# we make the decorator explicitly so we can reuse the same folds
# in both tuned and untuned approaches
folds = optunity.cross_validation.generate_folds(data.shape[0], num_folds=3)
outer_cv = optunity.cross_validated(x=data, y=labels, num_folds=3, folds=[folds],
                                    aggregator=optunity.cross_validation.identity)
outer_cv = optunity.cross_validated(x=data, y=labels, num_folds=3)

# compute area under ROC curve of default parameters
def compute_roc_standard(x_train, y_train, x_test, y_test):
    model = sklearn.svm.SVC().fit(x_train, y_train)
    decision_values = model.decision_function(x_test)
    auc = optunity.metrics.roc_auc(y_test, decision_values)
    return auc

# decorate with cross-validation
compute_roc_standard = outer_cv(compute_roc_standard)
roc_standard = compute_roc_standard()
#print('Nested cv area under ROC curve of non-tuned model: ' + str(roc_standard))

# compute area under ROC curve with tuned parameters
# we use 2x5 fold cross-validation while tuning
def compute_roc_tuned(x_train, y_train, x_test, y_test):

    # define objective function
    @optunity.cross_validated(x=x_train, y=y_train, num_iter=2, num_folds=5)
    def inner_cv(x_train, y_train, x_test, y_test, C, gamma):
        model = sklearn.svm.SVC(C=C, gamma=gamma).fit(x_train, y_train)
        decision_values = model.decision_function(x_test)
        return optunity.metrics.roc_auc(y_test, decision_values)

    # optimize parameters
    optimal_pars, _, _ = optunity.maximize(inner_cv, 150, C=[0, 10], gamma=[0, 0.1], pmap=optunity.pmap)
    # if you are running this in IPython, optunity.pmap will not work
    # more info at: https://github.com/claesenm/optunity/issues/8
    # comment out the above line and replace by the one below:
    # optimal_pars, _, _ = optunity.maximize(inner_cv, 200, C=[0, 10], gamma=[0, 0.1])

    tuned_model = sklearn.svm.SVC(**optimal_pars).fit(x_train, y_train)
    decision_values = tuned_model.decision_function(x_test)
    auc = optunity.metrics.roc_auc(y_test, decision_values)
    return auc

# decorate with cross-validation
compute_roc_tuned = outer_cv(compute_roc_tuned)

t = time.time()
roc_tuned = compute_roc_tuned()
diff = time.time() - t
print('Nested cv area under ROC curve of tuned model: ' + str(roc_tuned))
print('Tuning time (approx): ' + str(diff/3) + ' seconds') # we tuned 3 times
