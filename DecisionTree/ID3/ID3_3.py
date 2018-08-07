# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date: 2018-08-07 15:07:17

import sys
sys.path.append('../../MultiwayTree')
import csv
import math
import Tree
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


class DecisionTreeNode(Tree.TreeNode):
    def __init__(self, name, dataset, edgename):
        super(DecisionTreeNode, Tree.TreeNode.__init__(self, name))
        self.dataset = dataset
        self.edgename = edgename


class DecisonTree(Tree.MultiTree):
    def __init__(self, root_name='root', root_dataset=None, root_edge=None):
        super(DecisonTree, Tree.MultiTree.__init__(self, root_name))
        self.tree = DecisionTreeNode(root_name, root_dataset, root_edge)


class BuildTree(object):
    def __init__(self, root_name, dataset, features):
        # super(BuildTree, self).__init__(*args))
        self.root_name = root_name
        self.datapool = dataset
        self.features = features
        self.dt = DecisonTree(root_name=root_name,
                              root_dataset=self.datapool)

    def count_label_entropy(self, data, features):
        attribute_num = len(data[features[-1]])
        label_entropy = 0
        label_counter = Counter(data[features[-1]])
        for l, l_counter in label_counter.items():
            label_entropy -= (l_counter / attribute_num) * \
                math.log((l_counter / attribute_num), 2)
        print("label's entropy:", label_entropy)
        return label_entropy, attribute_num

    def information_entropy(self, data, feature, attribute):
        sub_attribute_entropy = {}
        att_group = data.groupby(attribute)
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

    def information_gain(self, data, feature, label_entropy, attribute_num):
        sub_attribute_entropy = self.information_entropy(
            data, feature, data[feature])
        Sigma_entropy = 0
        for attribute_name, attribute_count in Counter(data[feature]).items():
            Sigma_entropy += (attribute_count / attribute_num) * \
                sub_attribute_entropy[attribute_name]
        return label_entropy - Sigma_entropy

    def split_data(self, node):
        data = node.dataset
        label_entropy, attribute_num = self.count_label_entropy(
            data, self.features)
        best_gain = 0
        best_feature = 0
        for feature in self.features[:-1]:
            current_gain = self.information_gain(
                data, feature, label_entropy, attribute_num)
            if current_gain > best_gain:
                best_gain = current_gain
                best_feature = feature
        splitname = best_feature
        print(splitname)
        split_data_dict = data.groupby(splitname)
        self.features.remove(splitname)
        node.name = splitname
        node_id = 0
        for split_attr, spli_value in split_data_dict:
            new_node = DecisionTreeNode(
                name=str(node_id), dataset=spli_value, edgename=split_attr)
            del spli_value[splitname]
            self.dt.add(new_node, parent=node)
            node_id += 1
        for child_node in node.children:
            print(child_node.dataset)
            print(self.features)
            self.split_data(child_node)

    def build(self):
        node = self.dt.tree
        self.split_data(node)
        # self.dt.show_tree()
        # for data in self.datapool:
        # for node, value in self.tree.items():
        #     data = value['data']
        #     child = value['child']
        #     label_entropy, attribute_num = self.count_label_entropy(
        #         data, self.features)
        #     print(label_entropy)
        #     best_gain = 0
        #     best_feature = 0
        #     for feature in self.features[:-1]:
        #         current_gain = self.information_gain(
        #             data, feature, label_entropy, attribute_num)
        #         if current_gain > best_gain:
        #             best_gain = current_gain
        #             best_feature = feature
        #     splitname = best_feature
        #     split_data = data.groupby(splitname)
        #     split_attr_dcit = {}
        #     self.features.remove(splitname)
        #     pt(self.features)
        #     for split_attr, spli_value in split_data:
        #         split_attr_dcit[split_attr] = {}
        #         pt(split_attr)
        #         del spli_value[splitname]
        #         child[split_attr] = spli_value
        # pt(self.tree)
        pass


def main():
    dataset, features = load_data()
    bt = BuildTree('root', dataset, features)
    bt.build()
    # dtn = DecisionTreeNode('a', 'b', 'c')
    # dt = DecisonTree()
    # print(dt.if_node_exist)


if __name__ == '__main__':
    main()
