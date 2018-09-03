# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-09-02 17:58:35

import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def derivative_sigmoid(z):
    return z * (1 - z)


class Perception(object):
    def __init__(self, theta=0, bias=0):
        self.theta = theta
        self.bias = bias
        self.active_result = None
        self.input_x = None

    def percept(self, input_x):
        self.input_x = input_x
        self.active_result = sigmoid(np.sum(self.theta.dot(x.T)) + self.bias)
        return self.active_result

    def bw_percept(self, x_delta):
        return x_delta * derivative_sigmoid(self.active_result)

    def update_weight(self, last_layer_delta):
        self.theta += self.input_x.T.dot(last_layer_delta)


class Layer(object):
    def __init__(self, perception_num=3):
        self.perceptions = [Perception() for i in perception_num]

    def forward(self, x):
        forward_layer_output = []
        for perception in self.perceptions:
            layer_output.append(perception.percept(x))
        return np.array(forward_layer_output)

    def backward(self, x_delta):
        backward_layer_output = []
        for perception in self.perceptions:
            backward_layer_output.append(perception.bw_percept(x_delta))
        return backward_layer_output

    def update_perception_weight(self, last_layer_delta):
        for perception in self.perceptions:
            perception.update_weight(last_layer_delta)


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

    def add_hidden_layer(self, hidden_layer):
        self.hidden_layers.append(hidden_layer)
        self.layers = self.combo_layers()

    def forward(self):
        layer_ouput = self.layers[0].forward(self.X_train)
        for layer in self.layers[1:]:
            layer_ouput = layer.forward(layer_ouput)
        return layer_ouput

    def backward(self, layer_output):
        output_error = self.Y_train - layer_output
        inverse_layers = (self.layers[::-1])[1:]
        for i in range(len(inverse_layers)):
            inverse_layer = inverse_layers[i]
            output_error = inverse_layer.backward(output_error)
            if i + 1 < len(inverse_layer):
                next_inverse_layer = inverse_layer[i + 1]
                next_inverse_layer.update_perception_weight(output_error)


def main():
    pass


if __name__ == '__main__':
    main()
