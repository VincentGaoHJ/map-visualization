# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/4/30
@Author: Haojun Gao
@Description: 
"""

import os
import pandas
from os import walk


class Node:
    def __init__(self, node_dir, idStr):
        self.nodeSelf = node_dir
        self.result_dir = os.path.join(node_dir, "result")
        self.idStr = idStr


# 准备工作
def init(data_path):
    if not os.path.exists(data_path):
        raise Exception("找不到要可视化数据的文件夹")

    # 设置可视化结果要保存的文件夹
    visual_path = data_path + "-visualization"
    visual_path_data = os.path.join(visual_path, 'data')
    if not os.path.exists(visual_path):
        os.makedirs(visual_path)
    if not os.path.exists(visual_path_data):
        os.makedirs(visual_path_data)

    return visual_path, visual_path_data


def prepare(poi_path):
    # 读取初始景点文件，获得每一个景点的经纬度坐标
    data = pandas.read_csv(poi_path, sep='\t')

    data.drop(['type_id', 'id', 'page', 'father_name',
               'father_id', 'sub_page'], axis=1, inplace=True)

    data.rename(columns={'name': 'poi_name'}, inplace=True)

    data.head()  # 显示数据的前几行data

    return data


def main(node, visual_path_data, data):
    dataframe_list = []
    # walk会返回3个参数，分别是路径，目录list，文件list，你可以按需修改下
    for root, dirs, files in walk(node.nodeSelf):
        for file in files:
            if '-poi.csv' in file:
                file_path = root + "\\" + file
                dataframe = pandas.read_csv(file_path)  # 读取文件
                dataframe = dataframe.loc[:, ~dataframe.columns.str.contains(
                    '^Unnamed')]  # 删除文件中的index列
                dataframe = pandas.merge(dataframe, data)  # 将经纬度坐标添加进表格中

                file_name_list = file_path.split("\\")
                file_name = ''.join(filter(lambda s: isinstance(s, str) and len(
                    s) == 1 and s != "." or ".csv" in s, file_name_list))
                print(file_name_list)
                print(file_name)
                dataframe.to_csv(os.path.join(
                    visual_path_data, file_name), encoding="utf-8-sig")


if __name__ == "__main__":
    # 设置要可视化的文件夹
    data_path = ".\\2019-04-30-09-54-32"

    poi_path = '.\\data\\list_all_sub.txt'

    visual_path, visual_path_data = init(data_path)

    data = prepare(poi_path)

    # 创建对象
    root_node = Node(data_path, '')

    main(root_node, visual_path_data, data)
