import optunity
import optunity.metrics
import sklearn.svm

# score function: twice iterated 10-fold cross-validated accuracy
@optunity.cross_validated(x=data, y=labels, num_folds=10, num_iter=2)
def svm_mse(x_train, y_train, x_test, y_test, C, gamma):
    model = sklearn.svm.SVR(C=C, gamma=gamma).fit(x_train, y_train)
    y_pred = model.predict(x_test)
    return optunity.metrics.mse(y_test, y_pred)

# perform tuning
optimal_pars, _, _ = optunity.minimize(svm_mse, num_evals=200, C=[0, 10], gamma=[0, 1])

# train model on the full training set with tuned hyperparameters
optimal_model = sklearn.svm.SVR(**optimal_pars).fit(data, labels)
