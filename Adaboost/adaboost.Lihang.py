# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date: 2018-09-24 17:05:38

import math
import numpy as np
from pprint import pprint


def load_simp_data():
    datMat = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    class_labels = np.array([1, 1, 1, -1, -1, -1, 1, 1, 1, -1])
    return datMat, class_labels


class Adaboost(object):
    def __init__(self, data, class_labels, iter_num):
        self.data = data
        sorted_data = sorted(self.data)
        self.class_labels = class_labels
        self.iter_num = iter_num
        self.n = len(data)
        self.classifier = []
        self.D = np.array([1 / self.n]*self.n)
        self.split_points = [(sorted_data[i]+sorted_data[i+1]) /
                             2 for i in range(self.n) if i+1 <= self.n-1]

    def stump(self, sign, split_point):
        preLabel = np.array([1]*self.n)
        if sign == '<':
            preLabel[self.data < split_point] = -1
        else:
            preLabel[self.data >= split_point] = -1
        return preLabel

    def find_split_point(self):
        min_error = np.inf
        weak_classifier = {}
        for split_point in self.split_points:
            for sign in ['<', '>=']:
                pre_label = self.stump(sign, split_point)
                weighted_err = self.D.copy()
                weighted_err[pre_label == self.class_labels] = 0
                sum_err = np.sum(weighted_err)
                if sum_err < min_error:
                    min_error = sum_err
                    weak_classifier['error'] = min_error
                    weak_classifier['split_point'] = split_point
                    weak_classifier['sign'] = sign
                    weak_classifier['result'] = pre_label
                    weak_classifier['weight'] = weighted_err
        return weak_classifier

    def normalizing(self, alpha, G):
        z = []
        for j in range(self.n):
            w = self.D[j]
            y = self.class_labels[j]
            g = G[j]
            z.append(w*np.exp(-1*alpha*y*G))
        return np.sum(z)

    def update_weight(self, weak_classifier):
        G = weak_classifier['result']
        alpha = weak_classifier['alpha']
        Z = self.normalizing(alpha, G)
        for i in range(self.n):
            old_w = self.D[i]
            y = self.class_labels[i]
            g = G[i]
            new_w = (old_w/Z)*np.exp(-1*alpha*y*g)
            self.D[i] = new_w
        print('The weight of data has been updated:\n', self.D)

    def train(self):
        for iterator in range(self.iter_num):
            weak_classifier = self.find_split_point()
            current_err = weak_classifier['error']
            alpha = 0.5*math.log((1-current_err)/current_err)
            weak_classifier['alpha'] = alpha
            self.update_weight(weak_classifier)
            self.classifier.append(weak_classifier)
        pprint(self.classifier)

    def sig(self, y):
        if y > 0:
            return 1
        else:
            return -1

    def test(self, x):
        f = 0
        for weak_classifier in self.classifier:
            y = 1
            alpha = weak_classifier['alpha']
            split_point = weak_classifier['split_point']
            if weak_classifier['sign'] == '<':
                if x < split_point:
                    y = -1
            else:
                if x >= split_point:
                    y = -1
            f += alpha*y
        result = self.sig(f)
        print(result)
        return result


def main():
    data, class_labels = load_simp_data()
    ada = Adaboost(data, class_labels, 10)
    ada.train()

    err = 0
    for i in range(len(data)):
        y = ada.test(data[i])
        if y != class_labels[i]:
            err += 1
    print(err/len(data))


if __name__ == '__main__':
    main()
