#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: start.py
@time: 2019/3/29 14:39:21
@desc:

"""
import Queue


class Node(object):

    def __init__(self, key, val):
        self.key = key
        self.val = val


class Tree(object):

    def __init__(self, val=None):
        self.father = None
        self.left = None
        self.right = None
        self.val = val

    def __str__(self):
        return str(self.val)

    def __iter__(self):
        queue = Queue.Queue()
        queue.put(self)
        while True:
            try:
                node = queue.get_nowait()
                if node.left:
                    queue.put(node.left)
                if node.right:
                    queue.put(node.right)
                yield node.val
            except Queue.Empty:
                break

    @staticmethod
    def create_tree(array):
        if len(array) < 1:
            return

        queue = Queue.Queue()
        val = array[0]
        root = father = Tree(val)
        queue.put(father)

        a_l = len(array)
        for i in range(1, a_l, 2):

            val1 = val2 = None
            if i + 0 < a_l:
                val1 = array[i]
            if i + 1 < a_l:
                val2 = array[i + 1]

            father = queue.get()

            if val1:
                left_tree = Tree(val1)
                left_tree.father = father
                father.left = left_tree
                queue.put(left_tree)

            if val2:
                right_tree = Tree(val2)
                right_tree.father = father
                father.right = right_tree
                queue.put(right_tree)
        return root

    @staticmethod
    def create_tree_binarry(array):
        a_l = len(array)
        if a_l < 1:
            return

        mid = a_l / 2
        val = array[mid]
        root = Tree(val)
        root.left = Tree.create_tree_binarry(array[:mid])
        if root.left:
            root.left.father = root
        root.right = Tree.create_tree_binarry(array[mid+1:])
        if root.right:
            root.right.father = root

        return root

    def add_node(self, val):
        father = self
        while father:
            if val < father.val:
                if not father.left:
                    father.left = Tree(val)
                    father.left.father = father
                    break
                else:
                    father = father.left
            elif val > father.val:
                if not father.right:
                    father.right = Tree(val)
                    father.right.father = father
                    break
                else:
                    father = father.right
            else:
                break


def print_tree(tree):
    if isinstance(tree, Tree):
        for i in tree:
            print(i)


def start():
    a = []
    for i in range(11):
        a.append(i)

    # a = a[::-1]

    print(a)
    tree = Tree.create_tree(a)
    print_tree(tree)
    tree = Tree.create_tree_binarry(a)
    print_tree(tree)


def test():
    queue = Queue.Queue()
    for i in range(11):
        queue.put(i)

    while True:
        try:
            print(queue.get_nowait())
        except Queue.Empty as e:
            break


if __name__ == '__main__':
    start()
    # test()
