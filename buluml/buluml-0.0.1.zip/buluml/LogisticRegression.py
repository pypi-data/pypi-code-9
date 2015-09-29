# encoding=utf-8
__author__ = 'LoveLYJ'

# import area
from numpy import *
import math

class LogisticRegression(object):
    """
    Logistic Regression
    """
    def __init__(self):
        self.weight = None
        self.accu = -1.0

    def __sigmoid(self, x):
        return 1.0 / (1 + exp(-x))

    def fit(self, X, Y, alpha = 0.05, iter_cycle = 2000):
        """
        fit model
        :param X: (m, n) numpy.mat
        :param Y: (m, 1) numpy.mat
        :param alpha: alpha step value
        :param iter_cycle: 迭代次数
        :return:
        """
        m, n = shape(X)
        try:
            X = mat(X)
            Y = mat(Y).reshape((m, 1))
        except ValueError, IndexError:
            print 'ERROR'
            return
        # init ws
        self.weight = ones((n, 1))
        # iter
        for cycle in range(iter_cycle):
            error = Y - self.__sigmoid(X * self.weight)
            self.weight += alpha * X.T * error

    def predict(self, X_test, Y_test, threshold = 0.5):
        """
        predict
        提供Y_test可以计算self.accu，准确率
        :param X_test: 测试数据 (m, n)
        :return: tag value (m, 1)
        """
        m, n = shape(X_test)
        try:
            X = mat(X_test)
            Y = mat(Y_test).reshape((m, 1))
        except ValueError, IndexError:
            print 'ERROR'
            return
        # calc lab
        self.predict_mat = greater(self.__sigmoid(X * self.weight), threshold)
        self.accu = float(sum(equal(self.predict_mat, greater(Y, 0.5))) / m)
        return self.predict_mat

    def accuracy(self, Y):
        return self.accu




if __name__ == '__main__':
    model = LogisticRegression()
    data = loadtxt('../data/train.txt')
    x = data[:, :-1]
    y = data[:, -1]
    model.fit(x, y)
    test = loadtxt('../data/test.txt')
    x_t = test[:, :-1]
    y_t = test[:, -1]
    model.predict(x_t, y_t)
    print model.accu