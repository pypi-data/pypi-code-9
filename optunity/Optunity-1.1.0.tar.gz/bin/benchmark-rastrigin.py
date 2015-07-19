import math
import optunity
import hyperopt
import matplotlib.pyplot as plt
import collections
import random
import numpy as np
import cPickle as pickle

def rastrigin(x1, x2):
    A = 10
    x = (x1, x2)
    return 2 * A + sum(map(lambda x: x ** 2 - A * math.cos(2 * math.pi * x), x))

def process_calllog(log, minimize=True):
    bests = [log['values'][0]]

    for val in log['values']:
        if minimize:
            if val < bests[-1]: bests.append(val)
            else: bests.append(bests[-1])
        else:
            if val > bests[-1]: bests.append(val)
            else: bests.append(bests[-1])

    return bests[1:]


mean_and_ci = collections.namedtuple('mean_and_ci', ['median', 'lb', 'ub'])
def process_traces(traces, ci_width=0.95):
    n = len(traces)
    lbidx = int((1.0 - ci_width) / 2 * n)
    ubidx = int((ci_width + (1.0 - ci_width) / 2) * n)
    medianidx = int(n / 2)

    result = []
    for itr in zip(*traces):
        srt = sorted(itr)
        result.append(mean_and_ci(median=srt[medianidx], lb=srt[lbidx], ub=srt[ubidx]))

    return result

def process_traces_bootstrap(traces, ci_width, nboot=500):
    n = nboot
    lbidx = int((1.0 - ci_width) / 2 * n)
    ubidx = int((ci_width + (1.0 - ci_width) / 2) * n)
    medianidx = int(n / 2)

    result = []
    for itr in zip(*traces):
        arr = np.array(itr)
        def resampled_mean():
            resamp = np.random.choice(arr, size=arr.shape[0])
            return np.mean(resamp)
        bootstrap = [resampled_mean() for _ in range(nboot)]
        srt = sorted(bootstrap)
        result.append(mean_and_ci(median=srt[medianidx], lb=srt[lbidx], ub=srt[ubidx]))

    return result

def plot_results(results, color='b'):
    medians = map(lambda x: x.median, results)
    lbs = map(lambda x: x.lb, results)
    ubs = map(lambda x: x.ub, results)
    idx = range(1, len(results) + 1)
    plt.plot(idx, map(math.log10, medians), color=color, linewidth=2)
    print('dimensions %d %d %d' % (len(idx), len(lbs), len(ubs)))
    plt.fill_between(idx, map(math.log10, lbs), map(math.log10, ubs), color=color, alpha=0.3)



search = {'x1': [-5.12, 5.12], 'x2': [-5.12, 5.12]}
solvers = ['particle swarm', 'cma-es', 'random search']
solvers = ['particle swarm', 'random search', 'tpe']
colors = ['b', 'r', 'g']
traces = {solver: [] for solver in solvers}
numiter = 500
numevals = 520
for i in xrange(numiter):
    print('Iter %d / %d' % (i+1, numiter))
    for solver in solvers:
        if solver == 'tpe':
            def rastrigin_wrapper():
                call_log = []
                def wrapped(args):
                    x1, x2 = args
                    f = rastrigin(x1, x2)
                    if not call_log: call_log.append(f)
                    else: call_log.append(f if f < call_log[-1] else call_log[-1])
                    return f
                return wrapped, call_log

            f, call_log = rastrigin_wrapper()
            space = [hyperopt.hp.uniform('x1', -5.12, 5.12), hyperopt.hp.uniform('x2', -5.12, 5.12)]

            # used to modify random seed of TPE algorithm
            # can't seem to find how to configure it properly
            def algo(*args, **kwargs):
                return hyperopt.tpe.suggest(*args, seed=random.randint(0, 10000), **kwargs)

            best = hyperopt.fmin(f, space=space, algo=algo, max_evals=numevals)
            traces[solver].append(call_log)

        else:
            optimum, details, _ = optunity.minimize(rastrigin, num_evals=numevals,
                                                solver_name=solver, pmap=optunity.pmap,
                                                **search)
            trace = process_calllog(details.call_log)
            traces[solver].append(trace)

results = {solver: process_traces_bootstrap(traces[solver], 0.95) for solver in solvers}

with open('rastrigin.pkl', 'w') as f:
    pickle.dump({'results': results, 'traces': traces}, f)


print('Results available for %s.' % ", ".join(results.keys()))
for solver in solvers:
    print('%s: %s' % (solver, str(results[solver][-1])))

for solver, color in zip(solvers, colors):
    plot_results(results[solver], color)

#plot_results(pso_results)

plt.xlabel('number of evaluations')
plt.ylabel('minimal error')
axes = plt.gca()
axes.set_xlim([0, 500])
plt.show()
