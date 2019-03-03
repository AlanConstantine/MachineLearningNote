# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date: 2018-09-24 17:05:38

import math
import numpy as np
from pprint import pprint


def load_simp_data():
    data = np.matrix([[1, 2.1, 1],
                      [2, 1.1, 5],
                      [1.3, 1, 9],
                      [1, 1, 6],
                      [2, 1, 8]])
    class_labels = np.array([1, 1, -1, -1, 1])
    return data, class_labels


class Adaboost(object):

    def __init__(self, data, class_labels, iter_num):
        self.data = data
        self.class_labels = class_labels
        self.iter_num = iter_num
        self.m, self.n = self.data.shape
        self.classifier = []
        self.D = np.mat(np.full((1, self.m), 1 / self.m)).T

    def stump(self, sign, split_point, attribute):
        pre_label = np.mat(np.ones((self.m, 1)))
        if sign == '<':
            pre_label[attribute < split_point] = -1
        else:
            pre_label[attribute >= split_point] = -1
        return pre_label

    def find_split_point(self):
        min_error = np.inf
        weak_classifier = {}
        labels = np.mat(self.class_labels).T
        for d in range(self.n):
            attribute = self.data[:, d]
            sorted_data = sorted(attribute)
            split_points = [(sorted_data[i] + sorted_data[i + 1]) /
                            2 for i in range(self.m) if i + 1 <= self.m - 1]
            for split_point in split_points:
                for sign in ['<', '>=']:
                    pre_label = self.stump(sign, split_point, attribute)
                    weighted_err = self.D.copy()
                    weighted_err[pre_label == labels] = 0
                    sum_err = np.sum(weighted_err)
                    if sum_err < min_error:
                        min_error = sum_err
                        weak_classifier['error'] = min_error
                        weak_classifier['split_point'] = split_point
                        weak_classifier['sign'] = sign
                        weak_classifier['result'] = pre_label
                        weak_classifier['dimension'] = d
        return weak_classifier

    def normalizing(self, alpha, G):
        z = []
        for j in range(self.n):
            # print(np.array(self.D.T)[0])
            w = (np.array(self.D.T)[0])[j]
            y = self.class_labels[j]
            g = G[j]
            z.append(w * np.exp(-1 * alpha * y * G))
        return np.sum(z)

    def update_weight(self, weak_classifier):
        G = weak_classifier['result']
        alpha = weak_classifier['alpha']
        Z = self.normalizing(alpha, G)
        for i in range(self.n):
            old_w = self.D[i]
            y = self.class_labels[i]
            g = G[i]
            new_w = (old_w / Z) * np.exp(-1 * alpha * y * g)
            self.D[i] = new_w
        # print('The weight of data has been updated:\n', self.D, '\n')

    def train(self):
        for iterator in range(self.iter_num):
            weak_classifier = self.find_split_point()
            current_err = weak_classifier['error']
            alpha = 0.5 * math.log((1 - current_err) / current_err)
            weak_classifier['alpha'] = alpha
            self.update_weight(weak_classifier)
            self.classifier.append(weak_classifier)
        pprint(self.classifier)
        print()

    def sig(self, y):
        if y > 0:
            return 1
        else:
            return -1

    def test(self, x):
        f = 0
        x = np.array(x)[0]
        for weak_classifier in self.classifier:
            y = 1
            alpha = weak_classifier['alpha']
            split_point = weak_classifier['split_point']
            d = weak_classifier['dimension']
            if weak_classifier['sign'] == '<':
                if x[d] < split_point:
                    y = -1
            else:
                if x[d] >= split_point:
                    y = -1
            f += alpha * y
        result = self.sig(f)
        return result


def main():
    data, class_labels = load_simp_data()
    ada = Adaboost(data, class_labels, 100)
    ada.train()

    err = 0
    for i in range(len(data)):
        y = ada.test(data[i])
        if y != class_labels[i]:
            err += 1
    print(err / len(data))


if __name__ == '__main__':
    main()
