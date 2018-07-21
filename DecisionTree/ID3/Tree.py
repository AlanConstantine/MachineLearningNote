# -*- coding: utf-8 -*-
# @Author: Alan Lau
# @Date  : 2018-07-21 22:01:01


import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint as pt


class TreeNode(object):
    def __init__(self, name):
        self.name = name
        self.children = []


class Tree(object):
    def __init__(self):
        self.count = 0
        self.tree = TreeNode('root')
        self.search_result_parent = None
        self.search_result_children = None

    def add(self, node, parent='root'):
        if self.if_node_exist_recursion(self.tree, node.name, if_node_exist=False):
            print('Error: Node %s has already existed!' % node.name)
        else:
            if parent == 'root':
                root_children = self.tree.children
                root_children.append(node)
                self.tree.children = root_children
            self.add_recursion(parent, node, self.tree)
            print('Add node:%s sucessfully!' % node.name)

    def search(self, node):
        if self.if_node_exist_recursion(self.tree, node.name, if_node_exist=False):
            print('parent:')
            pt(self.search_result_parent)
            print('children:')
            pt(self.search_result_children)
        else:
            print("Error: Node %s doesn't exist!" % node.name)

    def to_dict(self, show_graph=False):
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

    def if_node_exist_recursion(self, tree, name, if_node_exist):
        if if_node_exist:
            return if_node_exist  # bug!!!!!!
        for child in tree.children:
            if child.name == name:
                if_node_exist = True
                self.search_result_parent = tree.name
                self.search_result_children = child.children
                self.count += 1
                # break
                print(if_node_exist)
                return if_node_exist
            else:
                self.if_node_exist_recursion(child, name, if_node_exist)
        # print(self.count)
        # return if_node_exist

    def add_recursion(self, parent, node, tree):
        for child in tree.children:
            if child.name == parent:
                children_list = child.children
                children_list.append(node)
                child.children = children_list
                break
            else:
                self.add_recursion(parent, node, child)


def main():
    T = Tree()
    A = TreeNode('A')
    B = TreeNode('B')
    C = TreeNode('C')
    D = TreeNode('D')
    T.add(A)
    T.add(D)
    T.add(B, 'A')
    T.add(C, 'A')
    # T.to_dict(show_graph=True)
    # T.add(A)
    T.add(C)


if __name__ == '__main__':
    main()
