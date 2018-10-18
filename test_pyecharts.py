#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_pyecharts.py
@time: 2017/12/23 13:45
@desc:

"""


import pyecharts


def func():

    page = pyecharts.Page()         # step 1

    # bar
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [5, 20, 36, 10, 75, 90]
    v2 = [10, 25, 8, 60, 20, 80]
    bar = pyecharts.Bar("柱状图数据堆叠示例")
    bar.add("商家A", attr, v1, is_stack=True)
    bar.add("商家B", attr, v2, is_stack=True)
    page.add(bar)         # step 2

    # scatter3D
    import random
    data = [[random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)] for _ in range(80)]
    range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
                   '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D = pyecharts.Scatter3D("3D 散点图示例", width=1200, height=600)
    scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
    page.add(scatter3D)  # step 2

    page.render()        # step 3

    # scatter_geo
    attr = ['11', '22']
    data = ['1', '2']
    scatter_geo = pyecharts.Geo("地理位置视图", width=1200, height=600)
    scatter_geo.add("", attr, data)
    page.add(scatter_geo)  # step 2

    page.render()        # step 3

    data = [["广州", "北京"], ["广州", "上海"]]
    scatter_geo = pyecharts.GeoLines("地理位置视图", width=1200, height=600)
    scatter_geo.add("上午航班", data, geo_normal_color='#ff00ff', geo_effect_period=9, geo_effect_color='#ff0000',
                    geo_effect_symbol='arrow')
    data = [["广州", "南昌"], ["广州", "成都"]]
    scatter_geo.add("下午航班", data, geo_effect_traillength=1,geo_emphasis_color='#0000ff')
    page.add(scatter_geo)  # step 2

    page.render()        # step 3


if __name__ == '__main__':
    func()
