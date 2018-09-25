# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date: 2018-09-24 17:05:38

import numpy as np


def loadSimpData():
    datMat = np.matrix([[1.,  2.1],
                        [2.,  1.1],
                        [1.3,  1.],
                        [1.,  1.],
                        [2.,  1.]])
    classLabels = np.matrix([1.0, 1.0, -1.0, -1.0, 1.0])
    return datMat, classLabels


class Adaboost(object):
    def __init__(self, datMat, classLabels):
        # super(Adaboost, self).__init__(*args))
        self.datMat = datMat
        self.classLabels = classLabels
        self.m, self.n = datMat.shape
        self.D = np.full((self.m, 1), 1 / self.m)

    def buildstump(self):
        for i in range(self.n):
            print(self.datMat[:, i])


def main():
    datMat, classLabels = loadSimpData()
    ada = Adaboost(datMat, classLabels)
    ada.buildstump()


if __name__ == '__main__':
    main()
