#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_yunci.py
@time: 2018/5/3 15:46
@desc:

"""


def start():
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    import jieba

    text_from_file_with_apath = open('1.txt').read()

    wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=True)
    wl_space_split = " ".join(wordlist_after_jieba)

    my_wordcloud = WordCloud().generate(wl_space_split)

    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    start()
