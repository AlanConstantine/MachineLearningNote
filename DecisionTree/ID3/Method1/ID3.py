# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date: 2018-08-07 15:07:17

import sys
sys.path.append('../../../MultiwayTree')
import csv
import math
import Tree
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from collections import Counter
from pprint import pprint as pt


'''
使用ID3算法，利用信息增益对属性进行划分；
构造树的方法是继承了MultiwayTree中的TreeNode和MultiTree。
'''


def load_data():
    f = open('../Watermelon.csv', 'r', encoding='utf8')
    csv_data = list(csv.reader(f))
    f.close()
    dataset = csv_data[1:]
    features = csv_data[0]
    return DataFrame(dataset, columns=features), features


class DecisionTreeNode(Tree.TreeNode):
    def __init__(self, name, dataset=[], edgename=None, node_result=None):
        super(DecisionTreeNode, Tree.TreeNode.__init__(self, name))
        self.dataset = dataset
        self.edgename = edgename
        self.node_result = node_result


class DecisonTree(Tree.MultiTree):
    def __init__(self, root_name='root', root_dataset=None, root_edge=None):
        super(DecisonTree, Tree.MultiTree.__init__(self, root_name))
        self.tree = DecisionTreeNode(root_name, root_dataset, root_edge)


class BuildTree(object):
    def __init__(self, root_name, dataset, features):
        self.root_name = root_name
        self.datapool = dataset
        self.features = features
        self.dt = DecisonTree(root_name=root_name,
                              root_dataset=self.datapool)

    def count_label_entropy(self, data, features):
        attribute_num = len(data[features[-1]])
        label_entropy = 0
        label_counter = Counter(data[features[-1]])
        if len(label_counter) == 1:
            return label_entropy, attribute_num, list(label_counter.keys())[0]
        for l, l_counter in label_counter.items():
            label_entropy -= (l_counter / attribute_num) * \
                math.log((l_counter / attribute_num), 2)
        print("label's entropy:", label_entropy)
        return label_entropy, attribute_num, None

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
        label_entropy, attribute_num, if_unique = self.count_label_entropy(
            data, self.features)
        if if_unique:
            node.name = node.edgename
            node.node_result = if_unique
            return 1
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
        for split_attr, spli_value in split_data_dict:
            if len(spli_value) == 0:
                # 因为当前结点包含的样本集为空集，不能划分，对应的处理措施为：将其设置为叶节点，类别为设置为其父节点所含样本最多的类别
                node_result = sorted(dict(Counter(
                    node.dataset[self.features[-1]])).items(), key=lambda x: x[1], reverse=True)[0][0]
                new_node = DecisionTreeNode(
                    name=split_attr, dataset=spli_value, edgename=split_attr, node_result=node_result)
            else:
                new_node = DecisionTreeNode(
                    name=split_attr, dataset=spli_value, edgename=split_attr)  # TODO
            del spli_value[splitname]
            self.dt.add(new_node, parent=node)
        for child_node in node.children:
            self.split_data(child_node)

    def build(self):
        node = self.dt.tree
        self.split_data(node)
        self.dt.show_tree()


def main():
    dataset, features = load_data()
    bt = BuildTree('root', dataset, features)
    bt.build()


if __name__ == '__main__':
    main()
