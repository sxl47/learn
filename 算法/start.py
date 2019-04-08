#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: start.py
@time: 2019/4/8 23:20
@desc:

"""


class Node(object):
    def __init__(self, val):
        self.val = val
        self.next = None


def print_lst_node(lst_node):
    lst = []
    while lst_node:
        lst.append(lst_node.val)
        lst_node = lst_node.next
    print lst


class Solution(object):
    def lengthOfLongestSubstring(self, s):

        """
        :type s: str
        :rtype: int
        """
        max_sub_str_len = 0
        length = len(s)
        for i in range(length):
            for j in range(i + 1, length + 1):
                sub_str = s[i:j]
                if j == length or s[j] in sub_str:
                    sub_str_len = j - i
                    if sub_str_len > max_sub_str_len:
                        max_sub_str_len = sub_str_len
                        print sub_str
                    break
        return max_sub_str_len

    def merge2Lists(self, list1, list2):
        """
        时间复杂度为：O(min(len(list1), len(lst2)))，这里用到循环，最大循环次数是根据最小链表长度来的，所以时间复杂度为：O(min(len(list1), len(lst2)))
        :type list1: List[ListNode]
        :type list2: List[ListNode]
        :rtype: ListNode
        """
        head_merge = list1 if list1.val < list2.val else list2
        main_node = head_merge
        tmp1_node = list2 if head_merge == list1 else list1
        tmp2_node = head_merge.next
        while tmp1_node and tmp2_node:
            if tmp1_node.val < tmp2_node.val:
                main_node.next = tmp1_node
                tmp1_node = tmp1_node.next
            else:
                main_node.next = tmp2_node
                tmp2_node = tmp2_node.next
            main_node = main_node.next
        if not tmp1_node:
            main_node.next = tmp2_node
        else:
            main_node.next = tmp1_node

        return head_merge


def start():
    s = Solution()
    n = s.lengthOfLongestSubstring('adbasfhi')
    print n

    lst1 = None
    lst2 = None
    tmp = None
    for i in range(2, 10, 2):
        node = Node(i)
        if not lst1:
            lst1 = node
            tmp = lst1
        else:
            tmp.next = node
            tmp = tmp.next

    for i in range(1, 9, 2):
        node = Node(i)
        if not lst2:
            lst2 = node
            tmp = lst2
        else:
            tmp.next = node
            tmp = tmp.next
    print_lst_node(lst1)
    print_lst_node(lst2)
    lst = s.merge2Lists(lst1, lst2)
    print_lst_node(lst)

    print 1


if __name__ == '__main__':
    start()
