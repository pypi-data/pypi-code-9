from concept_formation.trestle import TrestleTree
from concept_formation.utils import mean, std
from random import shuffle

def train(tree):
    shapes = ['circle', 'square', 'triangle', 'star']
    colors = ['yellow', 'green', 'blue', 'red']

    training = []
    for s in shapes:
        for c in colors:
            #if s == 'square' and c == 'blue':
            #    continue
            #if s == 'square' and c == 'green':
            #    continue
            #if s == 'circle' and c == 'green':
            #    continue

            e = {'shape': s, 'color': c}
            training.append(e)

    for i in range(5):
        shuffle(training)
        for e in training:
            tree.ifit(e)

def test(tree):
    shapes = ['circle', 'square', 'triangle', 'star']
    colors = ['yellow', 'green', 'blue', 'red']

    accuracy = []
    for s in shapes:
        for c in colors:
            #if s == 'square' and c == 'blue':
            #    continue
            #if s == 'square' and c == 'green':
            #    continue
            #if s == 'circle' and c == 'green':
            #    continue

            e = {'shape': s, 'color': c, 'experiment': 'yes'}

            if c == 'green':
                accuracy.append(tree.categorize(e).get_probability('is-chromium', 'yes'))
            else:
                accuracy.append(1 - tree.categorize(e).get_probability('is-chromium', 'yes'))
    return mean(accuracy)

negative = {'shape': 'square', 'color': 'blue', 'experiment': 'yes', 'is-chromium': 'no'}
HApositive = {'shape': 'square', 'color': 'green', 'experiment': 'yes', 'is-chromium': 'yes'}
LApositive = {'shape': 'circle', 'color': 'green', 'experiment': 'yes', 'is-chromium': 'yes'}
new = {'color': 'blue', 'experiment': 'yes'}

tree = TrestleTree()

ha = []
la = []

for i in range(100):
    tree.clear()
    train(tree)
    for j in range(1):
        tree.ifit(negative)
        tree.ifit(HApositive)
    ha.append(test(tree))

    tree.clear()
    train(tree)
    for j in range(1):
        tree.ifit(negative)
        tree.ifit(LApositive)
    la.append(test(tree))

print('ha: %0.2f (%0.2f)' % (mean(ha), std(ha)))
print('la: %0.2f (%0.2f)' % (mean(la), std(la)))

