#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-02 13:25:10
# @Version : Python2.7
# @Author  : AlanLau
# @Email   : rlalan@outlook.com
# @Blog    : http://blog.csdn.net/AlanConstantineLau

# from reader import readtxt as rt
# from distance import Edit_distance_array as ed
# from statistic import orderdic as od
import random


def edit_distance(str1, str2):
    str1_len = len(str1) + 1
    str2_len = len(str2) + 1
    matrix = [[0 for col in xrange(str2_len)] for row in xrange(str1_len)]
    for i in xrange(1, str1_len):
        matrix[i][0] = i
    for j in xrange(1, str2_len):
        matrix[0][j] = j
    for row in xrange(1, str1_len):
        for col in xrange(1, str2_len):
            cos = 0
            if str1[row - 1] == str2[col - 1]:
                cos = 0
            else:
                cos = 1
            matrix[row][col] = min(
                matrix[row - 1][col] + 1, matrix[row][col - 1] + 1, matrix[row - 1][col - 1] + cos)
    distance = matrix[-1][-1]
    return int(distance)


def clean_data(data):
    new_data = {}
    id = 0
    for datum in data:
        id += 1
        datum_list = datum.strip().split()
        new_data[id] = datum_list
    return new_data


def similarity(token1, token2):
    distance = edit_distance(token1, token2)
    return 1.0 - float(distance) / max(len(token1), len(token2))


def orderdic(dic, reverse):
    ordered_list = sorted(
        dic.items(), key=lambda item: item[1], reverse=reverse)
    return ordered_list


def single_pass(data):
    sim_sum = 0
    get_first_point = random.randint(1, len(data))
    category = {get_first_point: []}
    for datum in data:
        if datum == get_first_point:
            continue
        else:
            flag = 0
            sort_sim = {}
            # print len(category)
            for cate in category:
                sim = similarity(data[cate], data[datum])
                if sim > 0.01:
                    sort_sim[cate] = sim
                else:
                    flag = 1
            if flag == 1:
                category[datum] = []
                continue
            else:
                sort = orderdic(sort_sim, True)
                category[sort[0][0]].append(datum)
    return category


def readtxt(path, encoding):
    with open(path, 'r', encoding=encoding) as f:
        lines = f.readlines()
    return lines


def main():
    datapath = r'../BPtest.txt'
    data = readtxt(datapath, 'utf8')
    data = clean_data(data)
    print single_pass(data)


if __name__ == '__main__':
    main()
