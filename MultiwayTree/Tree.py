# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-07-21 22:01:01


import networkx as nx
from pprint import pprint as pt
import matplotlib.pyplot as plt


class TreeNode(object):
    '''
    树的节点
    '''

    def __init__(self, name):
        self.name = name
        self.children = []


class MultiTree(object):
    '''
    树的操作：
    增、删、改、查
    '''

    def __init__(self, tree_root_name='root'):
        self.count = 0
        self.tree = TreeNode(tree_root_name)
        self.if_node_exist = False
        self.search_result_parent = None
        self.search_result_children = []

    def add(self, node, parent=None):
        '''
        增加节点
        '''
        self.if_node_exist = False
        self.if_node_exist_recursion(
            self.tree, node, search=False, if_del=False)
        if self.if_node_exist:
            # 判断增加的节点是否原先就存在
            print('Error: Node %s has already existed!' % node.name)
            print('*' * 30)
        else:
            if parent == None:
                # 如果parent为None，则默认其父节点为root节点
                root_children = self.tree.children
                root_children.append(node)
                self.tree.children = root_children
                print('Add node:%s sucessfully!' % node.name)
                print('*' * 30)
            else:
                # 否则检查增加的节点的父节点是否存在
                self.if_node_exist = False
                self.if_node_exist_recursion(
                    self.tree, parent, search=False, if_del=False)
                if self.if_node_exist:
                    # 若父节点存在
                    self.add_recursion(parent.name, node, self.tree)
                    print('Add node:%s sucessfully!' % node.name)
                    print('*' * 30)
                else:
                    # 若父节点不存在
                    print("Error: Parent node %s doesn't exist!" % parent.name)
                    print('*' * 30)

    def search(self, node):
        '''
        检索节点
        打印出其父节点的name以及其下一层所有子节点的name
        '''
        self.if_node_exist = False
        self.if_node_exist_recursion(
            self.tree, node, search=True, if_del=False)
        if self.if_node_exist:
            # 若需要检索的节点存在，返回其父节点以及所有子节点
            print("%s's parent:" % node.name)
            pt(self.search_result_parent)
            print("%s's children:" % node.name)
            pt(self.search_result_children)
            print('*' * 30)
        else:
            # 若检索的节点不存在树中
            print("Error: Node %s doesn't exist!" % node.name)
            print('*' * 30)

    def delete(self, node):
        '''
        删除节点
        '''
        self.if_node_exist = False
        self.if_node_exist_recursion(
            self.tree, node, search=False, if_del=True)
        if not self.if_node_exist:
            print("Error: Node %s doesn't exist!" % node.name)
            print('*' * 30)
        else:
            print('Delete node %s sucessfully!' % node.name)
            print('*' * 30)

    def modify(self, node, new_parent=None):
        '''
        修改节点的父节点
        '''
        self.if_node_exist = False
        self.if_node_exist_recursion(
            self.tree, node, search=False, if_del=False)
        if not self.if_node_exist:
            # 判断需要修改的节点是否原先就存在
            print("Error: Node %s doesn't exist!" % node.name)
            print('*' * 30)
        else:
            if new_parent == None:
                # 如果new_parent为None，则默认其父节点为root节点
                self.if_node_exist = False
                self.if_node_exist_recursion(
                    self.tree, node, search=False, if_del=True)
                root_children = self.tree.children
                root_children.append(node)
                self.tree.children = root_children
                print('Modify node:%s sucessfully!' % node.name)
                print('*' * 30)
            else:
                # 否则检查需要修改的节点的父节点是否存在
                self.if_node_exist = False
                self.if_node_exist_recursion(
                    self.tree, new_parent, search=False, if_del=False)
                if self.if_node_exist:
                    # 若父节点存在
                    self.if_node_exist = False
                    self.if_node_exist_recursion(
                        self.tree, node, search=False, if_del=True)
                    self.add_recursion(new_parent.name, node, self.tree)
                    print('Modify node:%s sucessfully!' % node.name)
                    print('*' * 30)
                else:
                    # 若父节点不存在
                    print("Error: Parent node %s doesn't exist!" %
                          new_parent.name)
                    print('*' * 30)

    def to_dict(self, show_graph=False):
        '''
        利用networkx转换成图结构，方便结合matplotlib将树画出来
        '''
        G = nx.Graph()
        self.to_dcit_recursion(self.tree, G)
        if show_graph == True:
            nx.draw(G, with_labels=True)
            plt.show()
        # sp = dict(nx.all_pairs_shortest_path(G))
        # pt(sp)

    def to_dcit_recursion(self, tree, G):
        for child in tree.children:
            G.add_nodes_from([tree.name, child.name])
            G.add_edge(tree.name, child.name)
            self.to_dcit_recursion(child, G)

    def if_node_exist_recursion(self, tree, node, search, if_del):
        '''
        tree:需要判断是否存在node节点的树
        node:需要判断的节点
        search:当检索到该节点时是否返回该节点的父节点和所有子节点
        if_del:当检索到该节点时是否删除该节点
        '''
        name = node.name
        if self.if_node_exist:
            return 1
        for child in tree.children:
            if child.name == name:
                self.if_node_exist = True
                if search == True:
                    self.search_result_parent = tree.name
                    for cchild in child.children:
                        self.search_result_children.append(cchild.name)
                elif if_del == True:
                    tree.children.remove(node)
                break
            else:
                self.if_node_exist_recursion(child, node, search, if_del)

    def add_recursion(self, parent, node, tree):
        '''
        增加节点时使用的递归函数
        '''
        for child in tree.children:
            if child.name == parent:
                children_list = child.children
                children_list.append(node)
                child.children = children_list
                break
            else:
                self.add_recursion(parent, node, child)


def main():
    T = MultiTree('tree')
    A = TreeNode('A')
    B = TreeNode('B')
    C = TreeNode('C')
    D = TreeNode('D')
    E = TreeNode('E')
    N = TreeNode('N')
    G = TreeNode('G')
    T.add(A)
    T.add(D)
    T.add(B, A)
    T.add(C, A)
    T.add(E, C)
    T.add(TreeNode('F'))
    T.add(G)
    T.add(TreeNode('H'), G)
    T.add(A)
    T.add(C)
    T.add(D)
    T.search(A)
    T.delete(A)
    # T.add(TreeNode('I'), N)
    T.add(A)
    T.modify(A, G)
    T.to_dict(show_graph=True)


if __name__ == '__main__':
    main()
