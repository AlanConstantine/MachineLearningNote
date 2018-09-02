# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-09-02 17:58:35

import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


class Perception(object):
    def __init__(self, theta=0, bias=0):
        self.theta = theta
        self.bias = bias

    def percept(self, x):
        return sigmoid(np.sum(self.theta.dot(x.T)) + self.bias)


class Layer(object):
    def __init__(self, perception_num=3):
        self.perceptions = [Perception() for i in perception_num]

    def forward(self, x):
        forward_layer_output = []
        for perception in self.perceptions:
            layer_output.append(perception.percept(x))
        return np.array(forward_layer_output)

    def backward(self, x):
        pass


class NeuralNetwork(object):
    def __init__(self, X_train, Y_train):
        self.X_train = np.array(X_train, dtype=float)
        self.Y_train = np.array(Y_train, dtype=float)
        self.inputSize = self.X_train.shape[-1]
        self.outputSize = self.Y_train.shape[-1]
        self.inputLayer = Layer(self.inputSize)
        self.outputLayer = Layer(self.outputSize)
        self.hidden_layers = []
        self.layers = self.combo_layers()

    def combo_layers(self):
        layers = [self.inputLayer]
        if len(self.hidden_layers) != 0:
            layers.extend(self.hidden_layers)
        layers.append(self.outputLayer)
        return layers

    def train(self):
        layer_ouput = self.layers[0].forward(self.X_train)
        for layer in self.layers[1:]:
            layer_ouput = layer.forward(layer_ouput)


def main():
    pass


if __name__ == '__main__':
    main()
