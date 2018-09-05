# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-09-02 17:58:35

import math
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
        self.theta += self.input_x.T.dot(x_delta)
        x_error = x_delta.dot(self.theta.T)
        perception_delta = x_error * \
            derivative_sigmoid(self.active_result)
        return perception_delta


class Layer(object):

    def __init__(self, perception_num=3):
        self.perceptions = [Perception() for i in perception_num]

    def forward(self, x):
        forward_layer_output = []
        for perception in self.perceptions:
            layer_output.append(perception.percept(x))
        return np.array(forward_layer_output)

    def backward(self, x_delta, if_ouput_layer):
        backward_layer_output = []
        for perception in self.perceptions:
            backward_layer_output.append(
                perception.bw_percept(x_delta, if_ouput_layer))
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
        self.outputLayer = Layer(self.outputSize)
        self.layers = [self.outputLayer]
        self.use_expericence_layers()

    def use_expericence_layers(self):
        hidden_layers_num = int(
            math.sqrt(self.inputSize + self.outputSize) + 2) + 1
        for i in range(hidden_layers_num):
            self.layers.insert(0, Layer())

    def add_hidden_layer(self, hidden_layer):
        self.hidden_layers.insert(0, hidden_layer)

    def remove_hidden_layer(self, remove_hidden_layer_num):
        if remove_hidden_layer_num == len(self.layers) - 1 or remove_hidden_layer_num == -1:
            print('[Error]Can not remove output layer.')
        if len(self.layers) <= 2:
            print('[Error]Can not remove layer anymore.')
        del self.layers[remove_hidden_layer_num]

    def show_layers(self):
        print("Input layer's perceptions' number:", self.inputSize)
        i = 0
        for layer in self.layers[:-1]:
            print("Layer %s's perceptions' number: %s",
                  (str(i), str(len(layer))))
         print("Output layer's perceptions' number:", self.outputSize)

    def forward(self):
        layer_ouput = self.layers[0].forward(self.X_train)
        for layer in self.layers[1:]:
            layer_ouput = layer.forward(layer_ouput)
        return layer_ouput

    def backward(self, layer_output):
        output_error = self.Y_train - layer_output
        output_delta=output_error*derivative_sigmoid(layer_output)
        inverse_layers = (self.layers[::-1])[1:]
        for i in range(len(inverse_layers)):
            inverse_layer = inverse_layers[i]
            output_delta = inverse_layer.backward(output_delta)


def main():
    pass


if __name__ == '__main__':
    main()

