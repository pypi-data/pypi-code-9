import math
import operator as op
import numpy as np
import collections
import optunity
import optunity.score_functions
import matplotlib.pylab as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import axes3d

npos = 150
nneg = 300
d = 0.5


def generate(n, d=1):
    return np.random.randn(n, 2) + np.array([[d, 0.0]] * n)


def squared_distance(x1, x2, ratio):
    return sum(map(lambda x, y, z: z * (x - y) ** 2, x1, x2, [1.0, ratio]))


knn_model = collections.namedtuple('knn_model', ['k', 'ratio', 'x', 'y'])
def knn_train(x_train, y_train, k, ratio):
    return knn_model(int(k), ratio, x_train, y_train)

def knn_predict(knn, x_test):
    def predict_instance(instance):
        distances = map(lambda xt: squared_distance(instance, xt, knn.ratio),
                        knn.x)
        decval = sum(zip(*sorted(zip(distances, knn.y)))[1][:knn.k - 1])
        if decval > 0:
            return 1
        else:
            return -1
    return map(predict_instance, x_test)


x_train = np.vstack([generate(npos, d), generate(nneg, -d)])
y_train = np.array([1]*npos + [-1]*nneg)

x_test = np.vstack([generate(npos, d), generate(nneg, -d)])
y_test = np.array([1]*npos + [-1]*nneg)

k = 2
ratio = 1.0
knn = knn_train(x_train, y_train, k, ratio)
prediction = knn_predict(knn, x_test)

@optunity.cross_validated(x_train, y=y_train)
def knn_score(x_train, y_train, x_test, y_test, k, ratio):
    knn = knn_train(x_train, y_train, k, ratio)
    yhat = knn_predict(knn, x_test)
    return optunity.score_functions.accuracy(y_test, yhat)


f = optunity.wrap_constraints(knn_score, -1, lb_o={'k': 0.5, 'ratio': 0.0})

#solution, details, _ = optunity.maximize(f, 500, k=[0.5, 10], ratio=[0, 2])

box = {'k': [1, 20], 'ratio': [0.0, 5.0]}

#solver = optunity.make_solver('particle swarm', num_generations=20, num_particles=10, max_speed=0.03, **box)
suggestion = optunity.suggest_solver(200, solver_name='particle swarm', **box)
#suggestion = optunity.suggest_solver(200, solver_name='cma-es', **box)
#suggestion = optunity.suggest_solver(200, solver_name='nelder-mead', **box)
solver = optunity.make_solver(**suggestion)
solution, details = optunity.optimize(solver, f, pmap=optunity.parallel.pmap)


print('solution: ' + str(solution))
print('optimum: ' + str(details.optimum))
print('stats: ' + str(details.stats))



k_filt = [k for k, val in zip(details.call_log['args']['k'],
                              details.call_log['values'])
          if val > 0.1]
r_filt = [r for r, val in zip(details.call_log['args']['ratio'],
                              details.call_log['values'])
          if val > 0.1]
val_filt = filter(lambda x: x > 0.1, details.call_log['values'])

plot_vals = map(lambda x: -math.log(1.0-x, 2), val_filt)

fig = plt.figure()
fig.hold(True)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(k_filt, r_filt, plot_vals, c=zip(*enumerate(plot_vals))[0], cmap=mpl.cm.RdYlGn, alpha=1.0)
plt.xlabel('k')
plt.ylabel('ratio')
ax.set_zlabel(r'$-\log_2(error\ rate)$')
plt.title(r'(k=' + str(round(details.call_log['args']['k'][0],2)) + ', r=' + str(round(details.call_log['args']['ratio'][0],2)) + ', acc=' + str(round(details.call_log['values'][0],3)) +
          r') $\rightarrow$ (k=' + str(round(solution['k'],2)) + ', r=' + str(round(solution['ratio'],2)) + ', acc=' + str(round(details.optimum, 3)) + ')')
plt.show()

