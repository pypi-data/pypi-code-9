import numpy as np
import operator as op

results = {'random search': [], 'nelder-mead': [], 'particle swarm': [], 'cma-es': [], 'tree-parzen': []}

with open('optunity_vs_hyperopt.txt', 'r') as f:
    for line in f:
        line = line.replace("\t\t", "\t")
        chunks = line.split(' \t ')
        results[chunks[0]].append(float(chunks[2]))

del results['cma-es']
del results['nelder-mead']

keys = results.keys()
values = results.values()
matrix = np.array(values)
print(matrix.shape)

wins = np.argmax(matrix, axis=0)
print(wins)
winslist = wins.tolist()
wincounts = [winslist.count(x) for x in range(len(keys))]

for method, wincnt in zip(keys, wincounts):
    print('%s won %d times, mean auc=%1.3f' % (method, wincnt, 0))

means = np.mean(matrix, axis=1)

print()
for method, mean in zip(keys, means):
    print('%s has mean AUC %1.2f' % (method, 100*mean))

bests = np.max(matrix, axis=0)
maxdeltas = [np.max(bests - matrix[i,:]) for i in range(len(keys))]
avgdeltas = [np.mean(bests - matrix[i, :]) for i in range(len(keys))]
mediandeltas = [np.median(bests - matrix[i, :]) for i in range(len(keys))]

print()
for method, maxdelta in zip(keys, maxdeltas):
    print('%s has max delta %1.2f' % (method, 100*maxdelta))

print()
for method, avgdelta in zip(keys, avgdeltas):
    print('%s has avg delta %1.2f' % (method, 100*avgdelta))
# create rank matrix


print()
for method, mediandelta in zip(keys, mediandeltas):
    print('%s has median delta %1.2f' % (method, 100*mediandelta))

ranks = [zip(*sorted(enumerate(matrix[:,i]), key=op.itemgetter(1), reverse=True))[0]
         for i in range(matrix.shape[1])]

print(ranks)

print()
for method, rs in zip(keys, zip(*ranks)):
    mean = float(sum(rs)) / len(rs) + 1.0
    print('%s has mean rank %1.2f' % (method, mean))
