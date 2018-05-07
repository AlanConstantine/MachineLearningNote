#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-02 12:21:02
# @Author  : Alan Lau
# @Email   : rlalan@outlook.com

import numpy as np
import matplotlib.pyplot as plt


def load_Dataset(filename):
    """加载数据"""
    numFeat = len(open(filename).readline().split('\t')) - 1
    dataMat = []
    labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat


def normal_equation(X, Y):
    """正规方程求w"""
    Xmat = np.mat(X)
    Ymat = np.mat(Y)
    YT = Ymat.T
    xTx = Xmat.T.dot(Xmat)
    if np.linalg.det(xTx) == 0:
        print('Matrix can not be inverse')
    return xTx.I * Xmat.T * YT


def use_loess(testX, X, Y, k):
    """局部加权线性回归"""
    Xmat = np.mat(X)
    Ymat = np.mat(Y).T
    simpleNum = Xmat.shape[0]
    Ypre = np.zeros(simpleNum)
    for i in range(simpleNum):
        Ypre[i] = loess(testX[i], Xmat, Ymat, k, simpleNum)
    return Ypre


def loess(testX, Xmat, Ymat, k, simpleNum):
    """计算每个点的权重weights"""
    weights = np.eye(simpleNum)
    for j in range(simpleNum):
        diffMat = testX - Xmat[j, :]
        weights[j, j] = np.exp(diffMat * diffMat.T / (-2 * (k**2)))
    XTwX = Xmat.T * (weights * Xmat)
    ws = XTwX.I * (Xmat.T * (weights * Ymat))
    return testX * ws


def show_Data(X, Y, k):
    # Xcopy = np.mat(X).copy()
    # Xcopy.sort(0)
    # ws = normal_equation(X, Y)
    # Ypre = Xcopy.dot(ws)
    # plt.plot(Xcopy[:, 1], Ypre, c='b')
    plt.scatter(
        np.mat(X)[:, 1].flatten().A[0], np.mat(Y).flatten().A[0], c='r')
    Ypre = use_loess(X, X, Y, k)
    sorti = np.mat(X)[:, 1].argsort(0)
    Xsort = np.mat(X)[sorti][:, 0, :]
    plt.plot(Xsort[:, 1], Ypre[sorti])
    plt.show()


def main():
    k = 0.01
    dataMat, labelMat = load_Dataset('ex1.txt')
    show_Data(dataMat, labelMat, k)


if __name__ == '__main__':
    main()
