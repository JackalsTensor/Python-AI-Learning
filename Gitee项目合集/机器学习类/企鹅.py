"""
项目：企鹅分类(基于帕尔默企鹅数据集的物种分类项目)
具体步骤：
    1.加载数据集
    2.数据预处理(数据清洗)
    3.数据集划分
    4.特征工程(标准化)
    5.模型训练(使用K近邻即KNN分类算法构建分类模型，使用训练集完成模型拟合训练)
    6.模型预测
    7.模型评估
"""

import pandas as pd
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

#1.加载数据集
df=pd.read_csv("D:/PythonProject1/数据集/企鹅数据集/penguins.csv")
#print(df)   可事先浏览数据集
#2.数据预处理(数据清洗)
df=df[['species','bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g']]  #删除无用列
df=df.dropna()  #删除缺失值
X=df.drop(['species'],axis=1)   #删除标签列
y=df['species']   #获取标签列
#3.数据集划分
x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=0,stratify=y)   #训练集切分
#4.特征工程(采用标准化)
transfer=StandardScaler()
x_train=transfer.fit_transform(x_train)
x_test=transfer.transform(x_test)
#5.模型训练(采用交叉验证和网格搜索寻找最优超参)
estimator=KNeighborsClassifier()
param_dict={'n_neighbors':[i for i in range(1,11)]}
estimator=GridSearchCV(estimator,param_dict,cv=4)
estimator.fit(x_train,y_train)
best_k = estimator.best_params_['n_neighbors']
print(f'最优超参是{best_k}')
estimator = estimator.best_estimator_
#6.模型预测
y_predict=estimator.predict(x_test)
print(f'预测结果为{y_predict}')
#7.模型评估
print(f'准确率为{accuracy_score(y_test,y_predict)}')