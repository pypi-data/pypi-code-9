#!/usr/bin/env python

from __future__ import print_function
import optunity

def train(x, filler=''):
    print(filler + 'Training data:')
    for instance in x:
        print(filler + str(instance))

def predict(x, filler=''):
    print(filler + 'Testing data:')
    for instance in x:
        print(filler + str(instance))


data = list(range(9))

@optunity.cross_validated(x=data, num_folds=3)
def cved(x_train, x_test):
    train(x_train)
    predict(x_test)
    return 0.0

cved()


@optunity.cross_validated(x=data, num_folds=3)
def nested_cv(x_train, x_test):
    @optunity.cross_validated(x=x_train, num_folds=3)
    def inner_cv(x_train, x_test):
        train(x_train, '...')
        predict(x_test, '...')
        return 0.0
    inner_cv()
    predict(x_test)
    return 0.0

nested_cv()
