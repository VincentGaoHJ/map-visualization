# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/4/30
@Author: Haojun Gao
@Description: 
"""

# 加载pyecharts
import os
import re
import pandas
from os import walk
from pyecharts import Geo, Bar, Line, Overlap, EffectScatter, Map, Style, Page


def visualize(df, name):
    # 导入自定义的地点经纬度
    geo_cities_coords = {df.iloc[i]['poi_name']: [df.iloc[i]['lng'], df.iloc[i]['lat']]
                         for i in range(len(df))}  # 根据文件大小生成字典
    attr = list(df['poi_name'])  # 字典的每个键值
    value = list(df['poi_porb'])  # 由于量值的太大，换算以下(散点的颜色就是和这个想关的)
    style = Style(title_color="#fff", title_pos="center",
                  width=1200, height=600, background_color="#404a59")

    # 可视化
    geo = Geo(name, **style.init_style)
    geo.add("", attr, value, visual_range=[0.2, 1], symbol_size=10,
            visual_text_color="#fff", is_piecewise=True,
            is_visualmap=True, maptype='北京', visual_split_number=10,
            geo_cities_coords=geo_cities_coords)
    return geo


def prepare(dirs):
    file_path_list = []
    file_name_list = []
    dataframe_list = []
    # walk会返回3个参数，分别是路径，目录list，文件list，你可以按需修改下
    for root, _, files in walk(dirs):
        for file in files:
            if '.csv' in file:
                file_path = root + "\\" + file
                file_path_list.append(file_path)
                file_name = re.split(r'[\\.]\s*', file_path)
                file_name = ''.join(filter(lambda s: "-poi" in s, file_name))
                file_name_list.append(file_name)

                dataframe = pandas.read_csv(file_path)  # 读取文件
                dataframe_list.append(dataframe)

    return file_name_list, dataframe_list


if __name__ == "__main__":

    root = "2019-04-30-09-54-32"

    dirs = ".\\" + root + "-visualization\\data"

    file_name_list, dataframe_list = prepare(dirs)

    print(file_name_list)

    if len(file_name_list) != len(dataframe_list):
        raise Exception("数量不匹配，请检查代码")

    page = Page()
    for i in range(len(file_name_list)):
        geo = visualize(dataframe_list[i], file_name_list[i])
        page.add(geo)
    page.render(root + "-visualization\\Over All Visualization.html")
