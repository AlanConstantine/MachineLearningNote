# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date: 2018-09-19 23:59:37


import numpy as np


def loadSampData():
    datMat = np.matrix([[1, 5],
                        [2, 2],
                        [3, 1],
                        [4, 6],
                        [6, 8],
                        [6, 5],
                        [7, 9],
                        [8, 7],
                        [9, 8],
                        [10, 2]])
    classLabels = [1, 1, -1, -1, 1, -1, 1, 1, -1, -1]
    return datMat, classLabels


class Adaboost(object):
    def __init__(self, *args):
        # super(Adaboost, self).__init__(*args))
        self.classfier = [h1(), h2(), h3()]
        self.datMat, self.classLabels = loadSampData()

    def init_examples_weight(self):
        return np.array([1/len(self.classLabels)]*self.classLabels)

    def iterator(self):
        pass
