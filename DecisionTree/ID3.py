# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-07-05 23:56:36

import csv
import math
import numpy as np
from collections import Counter
from pprint import pprint as pt


def load_data():
    f = open('./Watermelon.csv', 'r', encoding='utf8')
    csv_data = list(csv.reader(f))
    f.close()
    dataset = csv_data[1:]
    features = csv_data[0][1:-1]
    dataset_T = list(zip(*dataset))
    return dataset, dataset_T[:-1], dataset_T[-1], features


class BuildTree(object):
    def __init__(self, dataset, dataset_T, labels, features):
        self.dataset = dataset
        self.dataset = dataset_T
        self.labels = labels
        self.features = features

    def information_entropy(self, sub_attributes, col):
        sub_attributes_set = {}
        for row in range(len(sub_attributes)):
            attribute = sub_attributes[row]
            if attribute in sub_attributes:
                pass
            else:
                pass


def main():
    dataset, dataset_T, labels, features = load_data()


if __name__ == '__main__':
    main()
