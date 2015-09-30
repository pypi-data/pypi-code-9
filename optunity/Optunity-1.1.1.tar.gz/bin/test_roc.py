import optunity.score_functions as score
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import random
import numpy.random

labels = [1]*1000 + [0]*1000
#preds = [random.normalvariate(0.5, 1) for _ in range(1000)] + [random.normalvariate(-0.5, 1) for _ in range(1000)]
labels = numpy.array(labels)

pos = numpy.random.normal(0.5, 1, 1000)
neg = numpy.random.normal(-0.5, 1, 1000)
preds = numpy.vstack((pos, neg))


fpr, tpr, _ = roc_curve(labels, preds)
scikit_roc =  auc(fpr, tpr)
optunity_roc = score.roc_auc(labels, preds, 1)

print('scikit AUROC:   ' + str(scikit_roc))
print('optunity AUROC: ' + str(optunity_roc))

prec, recall, _ = precision_recall_curve(labels, preds)
scikit_pr = auc(recall, prec)
optunity_pr = score.pr_auc(labels, preds, 1)

print('scikit AUPR:   ' + str(scikit_pr))
print('optunity AUPR: ' + str(optunity_pr))
