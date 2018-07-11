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
        self.attribute_num = len(self.dataset[self.features[-1]])
        self.label_entropy = self.count_label_entropy()

    def count_label_entropy(self):
        label_entropy = 0
        label_counter = Counter(self.dataset[self.features[-1]])
        for l, l_counter in label_counter.items():
            label_entropy -= (l_counter / self.attribute_num) * \
                math.log((l_counter / self.attribute_num), 2)
        print("label's entropy:", label_entropy)
        return label_entropy

    def information_entropy(self, attribute):
        sub_attribute_entropy = {}
        att_group = self.dataset.groupby(attribute)
        label_group = att_group[self.features[-1]]
        for a, l in label_group:
            l_counter_dict = Counter(l)
            l_num = len(l)
            entropy = 0
            for l, l_counter in l_counter_dict.items():
                entropy -= (l_counter / l_num) * \
                    math.log((l_counter / l_num), 2)
            sub_attribute_entropy[a] = entropy
        return sub_attribute_entropy

    def information_gain(self, feature):
        sub_attribute_entropy = self.information_entropy(self.dataset[feature])
        Sigma_entropy = 0
        for attribute_name, attribute_count in Counter(self.dataset[feature]).items():
            Sigma_entropy += (attribute_count / self.attribute_num) * \
                sub_attribute_entropy[attribute_name]
        return self.label_entropy - Sigma_entropy

    def count_entropy(self):
        information_gain_dict = {}
        for feature in self.features[:-1]:
            information_gain_dict[feature] = self.information_gain(feature)
        information_gain_dict_sorted = sorted(
            information_gain_dict.items(), key=lambda x: x[1], reverse=True)
        pt(information_gain_dict_sorted[0][0])
        # TODO


def main():
    dataset, features = load_data()
    bt = BuildTree(dataset, features)
    bt.count_entropy()


if __name__ == '__main__':
    main()
