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
    dataset_T = list(zip(*dataset))
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
            print(a, l_counter, l_num)
            for l, l_counter in l_counter_dict.items():
                pass

    def get_entropy(self):
        for attribute in self.dataset:
            self.information_entropy(attribute)
            break


def main():
    dataset, features = load_data()
    bt = BuildTree(dataset, features)
    bt.get_entropy()


if __name__ == '__main__':
    main()
