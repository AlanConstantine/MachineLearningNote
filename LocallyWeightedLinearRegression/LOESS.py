#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-02 12:21:02
# @Author  : Alan Lau
# @Email   : rlalan@outlook.com

import numpy as np
import matplotlib.pyplot as plt


def load_Dataset(filename):
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
    return np.mat(dataMat), np.mat(labelMat)


def normal_equation(Xmat, Ymat):
    YT = Ymat.T
    xTx = Xmat.T.dot(Xmat)
    if np.linalg.det(xTx) == 0:
        print('Matrix can not be inverse')
    return xTx.I * Xmat.T * YT


def use_loess(Xmat, Ymat):
    pass
    simpleNum = Xmat.shape[0]
    for i in range(simpleNum):
        pass


def show_Data(Xmat, Ymat):
    # Xcopy = Xmat.copy()
    # Xcopy.sort(0)
    # ws = normalEquation(Xmat, Ymat)
    use_loess(Xmat, Ymat)
    # Ypre = Xcopy.dot(ws)
    # plt.scatter(X[:, 1].flatten().A[0], Ymat.flatten().A[0], c='r')
    # plt.plot(Xcopy[:, 1], Ypre, c='b')
    # plt.show()


def main():
    dataMat, labelMat = load_Dataset('ex1.txt')
    show_Data(dataMat, labelMat)


if __name__ == '__main__':
    main()
