#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: ssort.py
@time: 2019/5/15 20:22
@desc:

"""
import random


def bubble_sort(lst_nums):
    """
    冒泡排序
    :param lst_nums:
    :return: 排好序的列表
    """
    lst_len = len(lst_nums)
    for i in range(lst_len):
        for j in range(i + 1, lst_len):
            if lst_nums[i] > lst_nums[j]:
                lst_nums[i], lst_nums[j] = lst_nums[j], lst_nums[i]
    return lst_nums


def select_sort(lst_nums):
    """
    选择排序
    :param lst_nums:
    :return: 排好序的列表
    """

    lst_len = len(lst_nums)
    for i in range(0, lst_len):
        min_i = i
        for j in range(i + 1, lst_len):
            if lst_nums[min_i] > lst_nums[j]:
                min_i = j

        lst_nums[i], lst_nums[min_i] = lst_nums[min_i], lst_nums[i]

    return lst_nums


def insert_sort(lst_nums):
    """
    插入排序
    :param lst_nums:
    :return: 排好序的列表
    """
    lst_len = len(lst_nums)
    for i in range(0, lst_len - 1):
        tmp = lst_nums[i + 1]
        j = i
        while j >= 0 and tmp < lst_nums[j]:
            lst_nums[j + 1] = lst_nums[j]
            j -= 1
        lst_nums[j + 1] = tmp
    return lst_nums


def shell_sort(lst_nums):
    """
    希尔排序
    :param lst_nums:
    :return:
    """
    lst_len = len(lst_nums)
    space = lst_len / 2
    while space > 0:
        begin = 0
        while begin < lst_len:
            for i in range(begin, begin + space - 1):
                tmp = lst_nums[i + 1]
                j = i
                while j >= 0 and tmp < lst_nums[j]:
                    lst_nums[j + 1] = lst_nums[j]
                    j -= 1
                lst_nums[j + 1] = tmp
            begin += space
        space /= 2
    return lst_nums


def quick_sort(lst_nums):
    """
    快速排序
    :param lst_nums:
    :return:
    """

    

    return lst_nums


def start():
    lst_nums = [x for x in range(10)]
    random.shuffle(lst_nums)
    print (lst_nums)
    # print (bubble_sort(lst_nums))
    # print (select_sort(lst_nums))
    # print (insert_sort(lst_nums))
    print (shell_sort(lst_nums))


if __name__ == '__main__':
    start()
