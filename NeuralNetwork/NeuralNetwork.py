# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-09-02 17:58:35

import math
import numpy as np
import matplotlib.pyplot as plt


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def derivative_sigmoid(z):
    return z * (1 - z)


class Perception(object):

    def __init__(self, inputSize, alpha=1):
        self.theta = np.random.randn(inputSize)
        self.alpha = alpha
        self.active_result = None
        self.input_x = None
        self.z = None

    def percept(self, input_x):
        self.input_x = input_x
        self.z = self.theta.dot(input_x.T)
        self.active_result = sigmoid(self.z)
        return sigmoid(self.z)

    def bw_percept(self, x_delta):
        # self.theta = self.theta + (self.alpha * (x_delta * self.input_x))
        x_error = x_delta * self.theta
        perception_delta = x_error * \
            derivative_sigmoid(self.z)

        self.theta = self.theta + (self.alpha * (x_delta * self.input_x))
        return perception_delta


class Layer(object):

    def __init__(self):
        self.perceptions = None
        self.inputSize = 3
        self.perception_num = 3

    def set_inputSize(self, inputSize):
        self.inputSize = inputSize

    def set_perceptionsNum(self, perception_num):
        self.perception_num = perception_num

    def set_perceptions(self):
        self.perceptions = [Perception(inputSize=self.inputSize)
                            for i in range(self.perception_num)]
        return self.perception_num

    def forward(self, x):
        forward_layer_output = []
        for perception in self.perceptions:
            forward_layer_output.append(perception.percept(x))
        return np.array(forward_layer_output)

    def backward(self, x_delta):
        backward_layer_output = []
        for perception in self.perceptions:
            backward_layer_output.append(
                perception.bw_percept(x_delta))
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
        self.layers = []

        firstLayer = Layer()
        firstLayer.set_inputSize(self.inputSize)
        perception_num = firstLayer.set_perceptions()

        outputLayer = Layer()
        outputLayer.set_perceptionsNum(self.outputSize)
        outputLayer.set_perceptions()

        self.layers = [firstLayer, outputLayer]

        for layer in self.layers[1:]:
            layer.set_inputSize(perception_num)
            perception_num = layer.set_perceptions()

    def forward(self, x):
        layer_ouput = self.layers[0].forward(x)
        for layer in self.layers[1:]:
            layer_ouput = layer.forward(layer_ouput)
        return layer_ouput

    def backward(self, layer_output, y):
        output_error = y - layer_output
        output_delta = output_error * derivative_sigmoid(layer_output)
        inverse_layers = (self.layers[::-1])[1:]
        for i in range(len(inverse_layers)):
            inverse_layer = inverse_layers[i]
            output_delta = inverse_layer.backward(output_delta)

    def train(self, iterate_num=100):
        iterate_axis = []
        loss_axis = []
        for i in range(iterate_num):
            total_error = 0
            for j in range(len(self.X_train)):
                x, y = self.X_train[j], self.Y_train[j]
                layer_output = self.forward(x)
                self.backward(layer_output, y)
                total_error = total_error + (y - layer_output)

            loss = ((total_error**2) / len(self.X_train))[0]
            print('Loss:', loss)

            iterate_axis.append(i + 1)
            loss_axis.append(loss)
        return iterate_axis, loss_axis

    def show_gradient(self, iterate_axis, loss_axis):
        plt.plot(iterate_axis, loss_axis, color='blue')
        plt.xlabel('Iterate number')
        plt.ylabel('Loss')
        plt.show()

    def predict(self):
        pass

 # def use_expericence_layers(self):
    #     hidden_layers_num = int(
    #         math.sqrt(self.inputSize + self.outputSize) + 2)
    #     for i in range(hidden_layers_num):
    #         self.layers.insert(1, Layer())

    # def add_hidden_layer(self, hidden_layer):
    #     self.hidden_layers.insert(0, hidden_layer)

    # def remove_hidden_layer(self, remove_hidden_layer_num):
    #     if remove_hidden_layer_num == len(self.layers) - 1 or remove_hidden_layer_num == -1:
    #         print('[Error]Can not remove output layer.')
    #     if len(self.layers) <= 2:
    #         print('[Error]Can not remove layer anymore.')
    #     del self.layers[remove_hidden_layer_num]

    # def show_layers(self):
    #     print("Input layer's perceptions' number:", self.inputSize)
    #     i = 0
    #     for layer in self.layers[:-1]:
    #         print("Layer %s's perceptions' number: %s" %
    #               (str(i), str(len(layer.perceptions))))
    #     print("Output layer's perceptions' number:", self.outputSize)


def main():
    # X = [[1, 1], [1, 0], [0, 1], [0, 0]]
    # Y = [[1], [1], [1], [0]]
    X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
    Y = np.array(([92], [86], [89]), dtype=float)
    X = X / np.amax(X, axis=0)
    Y = Y / 100
    nn = NeuralNetwork(X, Y)
    iterate_axis, loss_axis = nn.train(150)
    nn.show_gradient(iterate_axis, loss_axis)


if __name__ == '__main__':
    main()
