"""
Kaggle比赛项目：房价预测
该文件主要用于观测训练集的特征，判断是否需要进行数据清洗操作
"""
import numpy as np
import pandas as pd
#查看训练集的特征
train_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle房价预测赛事数据集\train.csv")
# print(train_df.info())
#根据训练集数据集无缺失值观测，发现有部分特征存在缺失问题.如果将有缺失值的行删去则可能造成大量数据损失，对此，我考虑将缺失值删除
#先挑出无缺失值的列并打印出列表
train_df_no_nan=train_df.dropna(axis=1)
# print(train_df_no_nan.columns)
#将训练集数据集进行重新赋值,完成训练集清洗缺失值的操作
train_df=train_df[train_df_no_nan.columns]
print(train_df.info())
#查看测试集特征
test_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle房价预测赛事数据集\test.csv")
# print(test_df.info())
#根据测试集数据集无缺失值观测，发现有部分特征存在缺失问题,同理对其进行缺失值处理
test_df_no_nan=test_df.dropna(axis=1)
test_df=test_df[test_df_no_nan.columns]
print(test_df.info())