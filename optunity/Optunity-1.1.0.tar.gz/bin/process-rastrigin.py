import cPickle as pickle
import matplotlib.pyplot as plt
import math
import collections
import csv

def plot_results(results, color='b'):
    medians = map(lambda x: x.median, results)
    lbs = map(lambda x: x.lb, results)
    ubs = map(lambda x: x.ub, results)
    idx = range(1, len(results) + 1)
    plt.plot(idx, map(math.log10, medians), color=color, linewidth=2)
    print('dimensions %d %d %d' % (len(idx), len(lbs), len(ubs)))
    plt.fill_between(idx, map(math.log10, lbs), map(math.log10, ubs), color=color, alpha=0.3)


mean_and_ci = collections.namedtuple('mean_and_ci', ['median', 'lb', 'ub'])
solvers = ['particle swarm', 'random search', 'tpe']
colors = ['b', 'r', 'g']

with open('rastrigin.pkl', 'r') as f:
    data = pickle.load(f)
    traces = data['traces']
    results = data['results']
    tpe = results['tpe']
    pso = results['particle swarm']
    rnd = results['random search']


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


def a_beats_b_idx(a, b):
    lst = [idx for idx, x, y in zip(xrange(1, int(1e6)), a, b) if x.ub < y.lb]
    return lst

tpe_beats_pso = a_beats_b_idx(tpe[:500], pso[:500])
pso_beats_tpe = a_beats_b_idx(pso[:500], tpe[:500])


solvermap = {'particle swarm': 'pso',
             'random search': 'rnd',
             'tpe': 'tpe'}

for solver in solvers:
    with open('%s.csv' % solvermap[solver], 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['iter','mean','lb','ub'])
        for idx, tup in enumerate(results[solver]):
            writer.writerow([idx+1, tup.median, tup.lb, tup.ub])

with open('tpe_beats_pso.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['iter'])
    for idx in tpe_beats_pso:
        writer.writerow([idx])

with open('pso_beats_tpe.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['iter'])
    for idx in pso_beats_tpe:
        writer.writerow([idx])
