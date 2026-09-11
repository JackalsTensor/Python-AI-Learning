#导包
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, root_mean_squared_error, mean_absolute_error
import numpy as np
import pandas as pd

""""
具体步骤：
    1.加载数据集
    2.数据预处理
    3.划分数据集
    4.特征工程
    5.模型训练
    6.模型预测
    7.模型评估
"""


#1.加载数据集(由于原数据不可用，本项目采用官方报错提示中的代码)
data_url="http://lib.stat.cmu.edu/datasets/boston"
raw_df=pd.read_csv(data_url,sep="\\s+",skiprows=22,header=None)
data=np.hstack([raw_df.values[::2,:],raw_df.values[1::2,:2]])
target=raw_df.values[1::2,2]
#print(data[:5])  事先浏览数据集
#2.数据预处理
#3.划分数据集
x_train,x_test,y_train,y_test = train_test_split(data,target,test_size=0.2,random_state=0)
#4.特征工程(标准化)
transfer=StandardScaler()
x_train=transfer.fit_transform(x_train)
x_test=transfer.transform(x_test)
#5.模型训练(正规方程法)
estimator=LinearRegression(fit_intercept= True)
estimator.fit(x_train,y_train)
print(f'权重为{estimator.coef_}')
print(f'偏置为{estimator.intercept_}')
#6.模型预测
y_predict=estimator.predict(x_test)
print(f'预测结果为{y_predict}')
#7.模型评估
print(f'均方误差为{mean_squared_error(y_test,y_predict)}')
print(f'均方根误差为{root_mean_squared_error(y_test,y_predict)}')
print(f'平均绝对误差为{mean_absolute_error(y_test,y_predict)}')