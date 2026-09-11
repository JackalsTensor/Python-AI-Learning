import numpy as np
import pandas as pd
df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle泰坦尼克号预测幸存者赛事数据集\Titanic-Train.csv")
#查看训练集特征列标签
print(df.columns)
#预览数据集
print(df.head())
#查看数据集信息
print(df.info())
#查看age缺失率
age_total = len(df['Age'])
age_missing = df['Age'].isnull().sum()
age_missing_rate = age_missing / age_total * 100
print(f'age缺失率：{age_missing_rate:.2f}%')