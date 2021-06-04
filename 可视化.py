#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/6 13:28
# @Author : loong
# @File : 可视化.py
# @Software: PyCharm

import pandas as pd
import numpy as np
import matplotlib
import re
import matplotlib.pyplot as plt

# 原始数据
data = pd.read_csv("information.csv", header=0, encoding="utf8", usecols=[1, 2, 3, 4, 5])  # 读取csv数据文件
# data = pd.DataFrame(data)
# print("Number of samples: %d" % len(data))
# data.fillna(0)


# 数据预处理
def type1(x):
    words1 = ['移动电源', '充电宝', '数据线', '音箱', '麦克风', '耳机', '手机壳', '钢化膜', '保护', '支架']
    for element in words1:
        if x.find(element) != -1:
            return (str('配件-') + element)
        elif x.find('二手') != -1:
            return ('二手手机')
    else:
        return ('新手机')



def type2(x):
    words1 = ['老人', '学生', '商务', '5G', '智能']
    for element in words1:
        if x.find(element) != -1:
            return (element + str('手机'))
    else:
        return ('智能手机')


def trans(c):
    if c.find('+') != -1:
        c = c.replace('+', '')
    if c.find('万') != -1:
        c = c.replace('万', '')
        c = float(c) * 10000
    c = str(int(c))
    return c



def check_contain_eng(check_str):
    if check_str.find('（') != -1 or check_str.find('）') != -1 or check_str.find('-') != -1:
        check_str = check_str.replace('（', '')
        check_str = check_str.replace('）', '')
        check_str = check_str.replace('-', '')
    if u'\u4e00' <= check_str <= u'\u9fff':
        check_str = re.sub('[a-zA-Z]', '', check_str)
    return str(check_str)


data["商品类型"] = data["info_name"].apply(type1)
data["info_commit"] = data["info_commit"].apply(trans)
data["info_commit"] = data["info_commit"].apply(pd.to_numeric)
data["info_brand"] = data["info_brand"].apply(check_contain_eng)
data["手机类型"] = data["info_name"].apply(type2)
data.fillna(0)

# 对数据进行数据类型的转换以及数据筛选
data['info_money'] = data['info_money'].astype(int)
data['info_commit'] = data['info_commit'].astype(int)
data1 = data[(data['商品类型'] == '新手机')]
data2 = data[(data['商品类型'] == '二手手机')]

# 不同品牌的评论量占比
font = {
    'family': 'SimHei',
    'size': 20
}
matplotlib.rc('font', **font);

plt.rcParams['figure.figsize'] = (20.0, 20.0)
gb1 = data1.groupby(
    by=['info_store'],
    as_index=False
)['info_commit'].agg({
    'info_commit': np.sum
});
g1 = gb1[gb1['info_commit'] > 2000000]
plt.pie(g1['info_commit'], labels=g1['info_store'], autopct='%0.1f%%');
plt.title('不同店铺销量分析')
plt.legend(loc='lower right',bbox_to_anchor=(1.2, 0, 0.5, 1))
plt.show()

# 不同店铺平均售价分析
gb1 = data1.groupby(
    by=['info_store'],
    as_index=False
)['info_money'].agg({
    'info_money': np.average
});
g1 = gb1[(gb1['info_money'] > 8000)]
index = np.arange(g1['info_store'].size);
plt.barh(index, g1['info_money'], height=0.5, color='Red');

plt.yticks(index, g1['info_store'],size=5)
plt.xlabel('售价8000元以上店铺平均售价分析',size=5)
plt.ylabel('商品售价',size=5)
plt.show()
# 不同价格区间购买人数
data1['info_money'] = data1['info_money'].astype(int)
bins = [min(data1['info_money']) - 1, 500, 1000, 3000, 5000, max(data1['info_money']) + 1];
labels = ['500及以下', '500到1000', '1000到3000', '3000到5000', '5000以上'];

# 价格分区 = pd.cut(data1['info_money'], bins, labels=labels)
# data1['info_money'] = 价格分区
jg = pd.cut(data1['info_money'], bins, labels=labels)
data1['info_money'] = jg
gb1 = data1.groupby(
    by=['info_money'],
    as_index=False
)['info_commit'].agg({
    'info_commit': np.sum
});
plt.pie(gb1['info_commit'], labels=gb1['info_money'], autopct='%.2f%%');
plt.title('不同价格区间购买人数百分比')
plt.show()


# 均价3000元以上手机品牌平均售价
data1 = data[(data['商品类型'] == '新手机')]
gb1 = data1.groupby(
    by=['info_brand'],
    as_index=False
)['info_money'].agg({
    'info_money': np.average
});

g1 = gb1[gb1['info_money'] > 3000]
index = np.arange(g1['info_brand'].size);
plt.bar(index, g1['info_money'], width=0.35, color='red');
plt.xticks(index, g1['info_brand'])
plt.xlabel('均价3000元以上手机品牌')
plt.ylabel('商品售价')
plt.show()

# 均价1000-3000元以上手机品牌平均售价
g2 = gb1[(gb1['info_money'] > 1000) & (gb1['info_money'] < 3000)]
index = np.arange(g2['info_brand'].size);
plt.bar(index, g2['info_money'], width=0.35, color='red');
plt.xticks(index, g2['info_brand'])
plt.xlabel('均价1000-3000元手机品牌')
plt.ylabel('商品售价')
plt.show()

# 散点图———————商品价格和购买人数关系
data3 = data[(data['商品类型'] == '新手机') & (data['info_money'] < 15000)]
plt.plot(data3['info_money'], data3['info_commit'], '.', color='blue')
plt.xlabel('商品售价')
plt.ylabel('购买人数')
plt.title('商品价格和购买人数关系')
plt.grid(True)
plt.show()

# 不同手机类型平均价格分析
data1 = data[(data['商品类型'] == '新手机')]
gb1 = data1.groupby(
    by=['手机类型'],
    as_index=False
)['info_money'].agg({
    'info_money': np.average
});

index = np.arange(gb1['手机类型'].size);
plt.bar(index, gb1['info_money'], width=0.35, color='red');
plt.xticks(index, gb1['手机类型'])
plt.xlabel('手机类型')
plt.ylabel('商品平均售价')
plt.legend(gb1)
plt.show()


# 不同手机类型购买人数占比分析
gb1 = data1.groupby(
    by=['手机类型'],
    as_index=False
)['info_commit'].agg({
    'info_commit': np.sum
});

plt.pie(gb1['info_commit'], labels=gb1['手机类型'], autopct='%0.01f%%');
plt.title('不同手机类型购买人数占比')
plt.legend(loc='lower right',bbox_to_anchor=(1.2, 0, 0.5, 1))
plt.show()
