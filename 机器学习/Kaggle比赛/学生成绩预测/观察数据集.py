"""
Kaggle比赛项目：对学生成绩进行预测
"""
#先观察数据集特征，预览数据集预先做出判断
import numpy as np
import pandas as pd

from 机器学习.Kaggle比赛.房价预测.观察数据集特征 import train_df

train_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle学生成绩预测赛事数据集\train (1).csv")
# print(train_df.info())
#观察数据集特征，发现无任何缺失值或者异常数据，因此不进行数据清洗
#查看测试集特征
test_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle学生成绩预测赛事数据集\test (1).csv")
print(test_df.info())
#观察数据集特征，发现无任何缺失值或者异常数据，因此不进行数据清洗