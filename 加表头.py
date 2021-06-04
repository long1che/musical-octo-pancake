#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/26 20:02
# @Author : loong
# @File : 加表头.py
# @Software: PyCharm

import pandas as pd
data=pd.read_csv(r'D:\xingkong\l\information.csv',header=None,names=["info_brand","info_name","info_money","info_store","info_commit"])
data.to_csv(r'D:\xingkong\l\information.csv')