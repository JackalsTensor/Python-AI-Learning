"""
案例：演示逻辑回归模型实现癌症预测
原理：把线性回归处理后的预测值通过Sigmoid测试函数，映射到[0,1]概率
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression  #逻辑回归模型
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from 机器学习.特征工程.特征预处理.标准化 import transfer

#1.加载数据
data = pd.read_csv(r"D:\PythonProject1\数据集\癌症预测数据集\breast_cancer_uci_original.csv")
# data.info () #显示数据集信息
#2.数据预处理
data.replace("?", np.nan, inplace=True)
data.dropna(axis=0,inplace=True)
# data.info()
#3.特征工程
X = data.iloc[:, 1:-1]
y=data.iloc[:, -1]
# print(X.shape, y.shape)
#数据集划分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=23)
transfer = StandardScaler()
X_train = transfer.fit_transform(X_train)
X_test = transfer.transform(X_test)
#4.模型训练
estimator = LogisticRegression()
estimator.fit(X_train, y_train)
#5.模型预测
y_predict = estimator.predict(X_test)
print(f'预测结果为{y_predict}')
#6.模型评估
print(f'准确率为{estimator.score(X_test, y_test)}')
print(f'准确率为{accuracy_score(y_test, y_predict)}')