# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-09-06 11:15:26

import numpy as np
import matplotlib.pyplot as plt

# X = (hours studying, hours sleeping), y = score on test, xPredicted = 4 hours studying & 8 hours sleeping (input data for prediction)
X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
y = np.array(([92], [86], [89]), dtype=float)
xPredicted = np.array(([4, 8]), dtype=float)

# scale units
X = X / np.amax(X, axis=0)  # maximum of X array
# maximum of xPredicted (our input data for the prediction)
xPredicted = xPredicted / np.amax(xPredicted, axis=0)
y = y / 100  # max test score is 100


class Neural_Network(object):
    def __init__(self):
        # parameters
        self.inputSize = 2
        self.outputSize = 1
        self.hiddenSize = 3

        # weights
        # (3x2) weight matrix from input to hidden layer
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        # (3x1) weight matrix from hidden to output layer
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)

    def forward(self, X):
        # forward propagation through our network
        # dot product of X (input) and first set of 3x2 weights
        self.z = np.dot(X, self.W1)
        self.z2 = self.sigmoid(self.z)  # activation function
        # dot product of hidden layer (z2) and second set of 3x1 weights
        self.z3 = np.dot(self.z2, self.W2)
        o = self.sigmoid(self.z3)  # final activation function
        return o

    def sigmoid(self, s):
        # activation function
        return 1 / (1 + np.exp(-s))

    def sigmoidPrime(self, s):
        # derivative of sigmoid
        return s * (1 - s)

    def backward(self, X, y, o):
        # backward propagate through the network
        self.o_error = y - o  # error in output
        # applying derivative of sigmoid to error
        self.o_delta = self.o_error * self.sigmoidPrime(o)

        # z2 error: how much our hidden layer weights contributed to output error
        self.z2_error = self.o_delta.dot(self.W2.T)
        # applying derivative of sigmoid to z2 error
        self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)

        # adjusting first set (input --> hidden) weights
        # print('self.z2_delta shape', self.z2_delta.shape)
        self.W1 += X.T.dot(self.z2_delta)
        # adjusting second set (hidden --> output) weights
        self.W2 += self.z2.T.dot(self.o_delta)

    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

    def saveWeights(self):
        np.savetxt("w1.txt", self.W1, fmt="%s")
        np.savetxt("w2.txt", self.W2, fmt="%s")

    def predict(self):
        print("Predicted data based on trained weights: ")
        print("Input (scaled): \n" + str(xPredicted))
        print("Output: \n" + str(self.forward(xPredicted)))


NN = Neural_Network()
it_axis = []
loss_axis = []
for i in range(1000):  # trains the NN 1,000 times
    # print("# " + str(i) + "\n")
    # print("Input (scaled): \n" + str(X))
    # print("Actual Output: \n" + str(y))
    # print("Predicted Output: \n" + str(NN.forward(X)))
    # mean sum squared loss
    print("Loss: " + str(np.mean(np.square(y - NN.forward(X)))))
    # print("\n")
    NN.train(X, y)
    it_axis.append(i + 1)
    loss_axis.append(np.mean(np.square(y - NN.forward(X))))
# plt.plot(it_axis, loss_axis, color='blue')
# plt.xlabel('Iterate number')
# plt.ylabel('Loss')
# plt.show()

# NN.saveWeights()
# NN.predict()
