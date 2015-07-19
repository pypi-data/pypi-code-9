import math
import numpy as np
from matplotlib import pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import sklearn.svm as svm
import sys

import optunity
import optunity.metrics

import hyperopt

plot = False
budget = 150
#budget = 200
#budget = 70

#search = {'C': [0, 10],
#          'gamma': [0, 5],
#          'beta0': [0, 10],
#          'beta1': [0, 10],
#          'beta2': [0, 10]}
search = {'C': [0, 10],
          'gamma': [0, 5],
          'beta0': [0, 7],
          'beta1': [0, 7],
          'beta2': [0, 7]}


# seed RNG
if len(sys.argv) > 1: np.random.seed(int(sys.argv[1]))

def printdict(d): return ", ".join(['%s=%1.3f' % (k, v) for k, v in sorted(d.items())])


def generate_spiral(n, start, radius, height, num_twists, noise_std):
    angle_step = float(num_twists * 2 * math.pi) / n
    height_step = float(height) / n
    spiral = np.array([map(lambda x: start[0] + radius * math.sin(angle_step * x + start[3]), range(n)),
                      map(lambda x: start[1] + radius * math.cos(angle_step * x + start[3]), range(n)),
                      map(lambda x: start[2] + height_step * x, range(n))])
    spiral = np.transpose(spiral)
    noise = np.dot(np.random.rand(n, 3), np.diag(np.array(noise_std)))
    return spiral + noise
#    return np.dot(spiral + noise, np.diag([1.0, 2.0, 1.0]))

n_train = 500
n_test = 5000
r = 1.0
h = 1.0
noise = (1.2, 1.0, 0.4)

pos_cfg = {'n': n_train,
               'start': (0.0, 0.0, 0.0, 0.0),
               'radius': r,
               'height': h,
               'num_twists': 2,
               'noise_std': noise}

train_pos = generate_spiral(**pos_cfg)
pos_cfg['n'] = n_test
test_pos = generate_spiral(**pos_cfg)

neg_cfg = {'n': n_train,
               'start': (0.0, 0.0, 0.0, math.pi),
               'radius': r,
               'height': h,
               'num_twists': 2,
               'noise_std': noise}
train_neg = generate_spiral(**neg_cfg)
neg_cfg['n'] = n_test
test_neg = generate_spiral(**neg_cfg)

if plot:
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(train_pos[:, 0], train_pos[:, 1], train_pos[:,2], 'bo', alpha=0.5)
    ax.plot(train_neg[:, 0], train_neg[:, 1], train_neg[:,2], 'ro', alpha=0.5)
    plt.show()

train_data = np.vstack((train_pos, train_neg))
train_labels = np.array([1] * train_pos.shape[0] + [0] * train_neg.shape[0])

test_data = np.vstack((test_pos, test_neg))
test_labels = np.array([1] * test_pos.shape[0] + [0] * test_neg.shape[0])



class elliptic_rbf_svm(object):
    def __init__(self, C=1.0, gamma=0.0, beta0=1.0, beta1=1.0, beta2=1.0):
        self._scaler = np.diag((beta0, beta1, beta2))
        self._C = C
        self._gamma = gamma
        self._model = svm.SVC(C=self._C, gamma=self._gamma, kernel='rbf')

    @property
    def scaler(self): return self._scaler

    @property
    def C(self): return self._C

    @property
    def gamma(self): return self._gamma

    @property
    def model(self): return self._model

    def fit(self, X, y):
        X_scaled = np.dot(X, self.scaler)
        self.model.fit(X_scaled, y)
        return self

    def predict(self, X):
        X_scaled = np.dot(X, self.scaler)
        return self.model.decision_function(X_scaled)


#@optunity.cross_validated(x=train_data, y=train_labels, num_folds=8, num_iter=3)
#@optunity.cross_validated(x=train_data, y=train_labels, num_folds=8, num_iter=2)
@optunity.cross_validated(x=train_data, y=train_labels, num_folds=10, regenerate_folds=True)
def svm_auc(x_train, y_train, x_test, y_test, C, gamma, beta0, beta1, beta2):
    model = elliptic_rbf_svm(C, gamma, beta0, beta1, beta2).fit(x_train, y_train)
    predictions = model.predict(x_test)
    return optunity.metrics.roc_auc(y_test, predictions, positive=1)

auc = svm_auc(C=1.0, gamma=0.0, beta0=1.0, beta1=1.0, beta2=1.0)
#print('default auc %f' % auc)

############ OPTUNITY: RANDOM SEARCH ###################

#method = 'grid search'
#optunity_best, info, _ = optunity.maximize(svm_auc, num_evals=budget, pmap=optunity.pmap,
#                                           solver_name=method, **search)
#
#model = elliptic_rbf_svm(**optunity_best).fit(train_data, train_labels)
#dvs = model.predict(test_data)
#test_auc = optunity.metrics.roc_auc(test_labels, dvs, positive=1)
#
#print('%s \t %f \t %f \t %s' % (method, info.optimum, test_auc, printdict(optunity_best)))

############ OPTUNITY: RANDOM SEARCH ###################

method = 'random search'
optunity_best, info, _ = optunity.maximize(svm_auc, num_evals=budget, pmap=optunity.pmap,
                                           solver_name=method, **search)

model = elliptic_rbf_svm(**optunity_best).fit(train_data, train_labels)
dvs = model.predict(test_data)
test_auc = optunity.metrics.roc_auc(test_labels, dvs, positive=1)

print('%s \t %f \t %f \t %s' % (method, info.optimum, test_auc, printdict(optunity_best)))

############ OPTUNITY: NELDER-MEAD ###################

#method = 'nelder-mead'
#optunity_best, info, _ = optunity.maximize(svm_auc, num_evals=budget, pmap=optunity.pmap,
#                                           solver_name=method, **search)
#
#model = elliptic_rbf_svm(**optunity_best).fit(train_data, train_labels)
#dvs = model.predict(test_data)
#test_auc = optunity.metrics.roc_auc(test_labels, dvs, positive=1)
#
#print('%s \t %f \t %f \t %s' % (method, info.optimum, test_auc, printdict(optunity_best)))

############ OPTUNITY: PARTICLE SWARM ###################

method = 'particle swarm'
optunity_best, info, _ = optunity.maximize(svm_auc, num_evals=budget, pmap=optunity.pmap,
                                           solver_name=method, **search)

model = elliptic_rbf_svm(**optunity_best).fit(train_data, train_labels)
dvs = model.predict(test_data)
test_auc = optunity.metrics.roc_auc(test_labels, dvs, positive=1)

print('%s \t %f \t %f \t %s' % (method, info.optimum, test_auc, printdict(optunity_best)))

############ OPTUNITY: CMA-ES ###################

method = 'cma-es'
optunity_best, info, _ = optunity.maximize(svm_auc, num_evals=budget, pmap=optunity.pmap,
                                           solver_name=method, **search)


model = elliptic_rbf_svm(**optunity_best).fit(train_data, train_labels)
dvs = model.predict(test_data)
test_auc = optunity.metrics.roc_auc(test_labels, dvs, positive=1)

print('%s \t \t %f \t %f \t %s' % (method, info.optimum[0], test_auc, printdict(optunity_best)))

############# HYPEROPT ####################

method = 'tree-parzen'
space = [hyperopt.hp.uniform('C', *search['C']), hyperopt.hp.uniform('gamma', *search['gamma']),
         hyperopt.hp.uniform('beta0', *search['beta0']), hyperopt.hp.uniform('beta1', *search['beta1']),
         hyperopt.hp.uniform('beta2', *search['beta2'])]

# hyperopt minimizes, not maximizes
def objective(tpl):
    return -svm_auc(C=tpl[0], gamma=tpl[1], beta0=tpl[2], beta1=tpl[3], beta2=tpl[4])

hyperopt_best = hyperopt.fmin(objective, space, algo=hyperopt.tpe.suggest, max_evals=budget)
model = elliptic_rbf_svm(**hyperopt_best).fit(train_data, train_labels)
dvs = model.predict(test_data)
test_auc = optunity.metrics.roc_auc(test_labels, dvs, positive=1)
print('%s \t %f \t %f \t %s' % (method, 0.0, test_auc, printdict(hyperopt_best)))
