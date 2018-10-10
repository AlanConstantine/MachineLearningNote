#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-29 22:47:19
# @Author  : Alan Lau
# @Email   : rlalan@outlook.com

import math
import numpy as np
import matplotlib.pyplot as plt


def sigmoid(func):
    """sigmoid函数"""
    return 1/(1+np.exp(-1*func))


def linear(a, b, X):
    """线性模型"""
    return a + b * X


def cost_function(Y, Ypre):
    """代价函数"""
    return (np.sum(np.square(Y - Ypre)) / len(Y)) / 2


def feature_scaling(feature):
    """特征缩放"""
    return (feature - np.mean(feature)) / (max(feature) - min(feature))


def derivative_a(Y, a, b, X):
    # 根据导数的基本原理进行求导
    return ((np.sum(np.square(Y - sigmoid(linear(a+0.0001, b, X)))) / len(Y)) / 2)/0.0001


def derivative_b(Y, a, b, X):
    return ((np.sum(np.square(Y - sigmoid(linear(a, b+0.0001, X)))) / len(Y)) / 2)/0.0001


def iterator(X, Y, a, b, alpha, iter_n):
    """迭代器"""
    Y = feature_scaling(Y)
    X = feature_scaling(X)
    Ypre = sigmoid(linear(a, b, X))
    error_function_list = []
    for i in range(iter_n):
        a_d = a - alpha * derivative_a(Y, a, b, X)
        b_d = b - alpha * derivative_b(Y, a, b, X)
        a = a_d
        b = b_d
        Ypre = sigmoid(linear(a, b, X))
        error_function_list.append(cost_function(Y, Ypre))
    return error_function_list


def show_data(e_f_l, iter_n):
    iterator_list = np.arange(iter_n)
    plt.plot(iterator_list, e_f_l, color='blue')
    plt.xlabel('iterate number')
    plt.ylabel('cost function')
    plt.show()


def main():
    X = [1400, 1600, 1700, 1875, 1100, 1550, 2350, 2450, 1425, 1700]
    # House size

    Y = [
        245000, 312000, 279000, 308000, 199000, 219000, 405000, 324000, 319000,
        255000
    ]
    # House prize
    a = 0.45
    b = 0.75
    X = np.array(X)
    Y = np.array(Y)
    alpha = 0.01
    iter_n = 100
    error_function_list = iterator(X, Y, a, b, alpha, iter_n)
    show_data(error_function_list, iter_n)


if __name__ == '__main__':
    main()
