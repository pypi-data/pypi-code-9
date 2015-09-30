import optunity as opt
import optunity.score_functions as score
import sklearn.svm
import numpy as np
import operator as op

npos = 400
nneg = 400
d = 0.5
scale = 10

# train data
train_data = np.vstack([np.random.randn(npos, 2) + np.array([[d, 0.0]] * npos),
                        np.random.randn(nneg, 2) - np.array([[d, 0.0]] * nneg)])
train_labels = [1] * npos + [-1] * nneg

# test data
test_data = np.vstack([np.random.randn(npos, 2) + np.array([[d, 0.0]] * npos),
                       np.random.randn(nneg, 2) - np.array([[d, 0.0]] * nneg)])
test_labels = [1] * npos + [-1] * nneg

train_data = scale * train_data
test_data = scale * test_data

def manual_tune(svm_acc):
    acc_list = []
    gamma_list = []
    c_list = []
    while True:
        print('')
        print('gamma?')
        gamma = input()
        print('gamma=' + str(gamma))
        print('C?')
        c = input()
        print('ca=' + str(c))
        acc = svm_acc(C=c, gamma=gamma)
        print('cv accuracy: ' + str(acc))

        acc_list.append(acc)
        gamma_list.append(gamma)
        c_list.append(c)

        print('')
        print('current log')
        print('===========')
        print('accuracy, c, gamma')
        for acc, c, gamma in sorted(zip(acc_list, c_list, gamma_list)):
            print(str(acc) + ', ' + str(c) + ', ' + str(gamma))

        print('')
        print('again?')
        again = input()
        if not again:
            break

    best_idx = max(enumerate(acc_list), key=op.itemgetter(1))[0]
    print('Manual tuning result')
    print('====================')
    print('gamma=' + str(gamma_list[best_idx]))
    print('c=' + str(c_list[best_idx]))
    print('accuracy=' + str(acc_list[best_idx]))
    return {'C': c_list[best_idx], 'gamma': gamma_list[best_idx]}, acc_list[best_idx]


@opt.cross_validated(x=train_data, y=train_labels,
                     num_folds=5, num_iter=2)
def svm_acc(x_train, y_train, x_test, y_test, C, gamma):
    model = sklearn.svm.SVC(C=C, gamma=gamma).fit(x_train, y_train)
    y_pred = model.predict(x_test)
    return score.accuracy(y_test, y_pred)


def grid_search(svm_acc, gammas, Cs):
    best_acc = 0.0
    best_c = None
    best_gamma = None
    for gamma in gammas:
        for C in Cs:
            acc = svm_acc(gamma=gamma, C=C)
            if acc > best_acc:
                best_acc = acc
                best_c = C
                best_gamma = gamma
    return {'C': best_c, 'gamma': best_gamma}, best_acc

manual_pars, manual_acc = manual_tune(svm_acc)
print('manual pars: ' + str(manual_pars))
print('manual acc: ' + str(manual_acc))

manual_model = sklearn.svm.SVC(**manual_pars).fit(train_data, train_labels)
manual_test_acc = score.accuracy(test_labels, manual_model.predict(test_data))
print('manual test acc: ' + str(manual_test_acc))

grid_pars, grid_acc = grid_search(svm_acc, [2**(e/2) for e in range(-8, 4)],
                                  [2**(e/2) for e in range(-8, 4)])
print('grid pars: ' + str(grid_pars))
print('grid acc: ' + str(grid_acc))

grid_model = sklearn.svm.SVC(**grid_pars).fit(train_data, train_labels)
grid_test_acc = score.accuracy(test_labels, grid_model.predict(test_data))
print('grid test acc: ' + str(grid_test_acc))


optunity_pars, info, _ = opt.maximize(svm_acc, num_evals=100, C=[0, 4], gamma=[0, 4])
optunity_acc = info.optimum
print('optunity pars: ' + str(optunity_pars))
print('optunity acc: ' + str(optunity_acc))

optunity_model = sklearn.svm.SVC(**optunity_pars).fit(train_data, train_labels)
optunity_test_acc = score.accuracy(test_labels, optunity_model.predict(test_data))
print('optunity test acc: ' + str(optunity_test_acc))
