"""
Kaggle预测客户流失
步骤：
   1.加载数据集
   2.数据预处理
   3.划分数据集
   4.特征工程
   5.模型训练
   6.模型评估
   7.模型预测
   8.提交示例
"""
import numpy as np
import pandas as pd

train_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle预测客户流失数据集\train.csv")
print(train_df.info())