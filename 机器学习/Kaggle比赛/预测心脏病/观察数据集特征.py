"""
项目:Kaggle预测心脏病
具体步骤：
    1.加载数据集
    2.数据预处理
    3.划分数据集
    4.特征工程
    5.模型训练(逻辑回归)
    6.模型评估
    7.模型预测
    8.提交示例
"""
#先提前观察数据集特征，预览数据集预先做出判断
import numpy as np
import pandas as pd
#查看训练集特征
train_df=pd.read_csv(r"D:\PythonProject1\数据集\kaggle预测心脏病赛事数据集\train.csv")
# print(train_df.info())     #观察数据集特征，发现无任何缺失值或者异常数据且文本数据，因此不进行数据清洗和热编码处理
#查看测试集特征
test_df=pd.read_csv(r"D:\PythonProject1\数据集\kaggle预测心脏病赛事数据集\test.csv")
print(test_df.info())        #观察数据集特征，发现无任何缺失值或者异常数据且文本数据，因此不进行数据清洗和热编码处理