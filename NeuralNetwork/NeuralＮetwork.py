# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-09-02 17:58:35

import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def perception(weight, theta, x):
    return sigmoid(weight * x + theta)


class Perception(object):
    def __init__(self, weight=0, theta=0):
        # super(Perception, self).__init__(*args))
        self.weight = weight
        self.theta = theta

    def pass


class Layer(object):
    def __init__(self, perception_num, x):
        # super(Layer, self).__init__(*args))
        self.perception = []


class NeuralNetwork(object):
    def __init__(self, X_train, Y_train):
        # super(NerualNet, self).__init__(*args))
        self.X_train = np.array(X_train, dtype=float)
        self.Y_train = np.array(Y_train, dtype=float)
        self.inputSize = self.X_train.shape[-1]
        self.outputSize = self.Y_train.shape[-1]
        self.hidden_layers = []
        pass


def main():
    pass


if __name__ == '__main__':
    main()
