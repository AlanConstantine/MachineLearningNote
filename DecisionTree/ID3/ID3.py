# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-07-05 23:56:36

import csv
import math
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from collections import Counter
from pprint import pprint as pt


def load_data():
    f = open('./Watermelon.csv', 'r', encoding='utf8')
    csv_data = list(csv.reader(f))
    f.close()
    dataset = csv_data[1:]
    features = csv_data[0]
    return DataFrame(dataset, columns=features), features


class BuildTree(object):
    def __init__(self, dataset, features):
        self.dataset = dataset
        self.dataset_T = dataset.T
        self.features = features

    def information_entropy(self, attribute):
        sub_attribute_entropy = {}
        att_group = self.dataset.groupby(attribute)
        label_group = att_group[self.features[-1]]
        for a, l in label_group:
            l_counter_dict = Counter(l)
            l_num = len(l)
            entropy = 0
            for l, l_counter in l_counter_dict.items():
                entropy -= (l_counter/l_num)*math.log((l_counter/l_num), 2)
            sub_attribute_entropy[a] = entropy
        print(sub_attribute_entropy)

    def information_gain(self):
        label_counter = Counter(self.dataset[self.features[-1]])
        label_entropy = 0
        l_num = len(self.dataset[self.features[-1]])
        for l, l_counter in label_counter.items():
            label_entropy -= (l_counter/l_num)*math.log((l_counter/l_num), 2)
        print(label_entropy)
        for feature in self.features[:-1]:
            self.information_entropy(self.dataset[feature])
            attribute_counter = Counter(self.dataset[feature])

    def get_entropy():
        pass


def main():
    dataset, features = load_data()
    bt = BuildTree(dataset, features)
    bt.get_entropy()


if __name__ == '__main__':
    main()
