""""
项目：鸢尾花的分类(额外添加了交叉验证和网格搜索，找出最优超参K使模型更好)
具体步骤：
    1.加载鸢尾花数据集(以python自带的鸢尾花数据集进行分析)
    2.对数据集进行预处理
    3.划分数据集
    4.特征工程(标准化)
    5.模型训练(使用K近邻即KNN分类算法构建分类模型，使用训练集完成模型拟合训练)
    6.模型评估
    7，模型预测
"""
"""
0: Setosa（山鸢尾）
1: Versicolor（变色鸢尾）
2: Virginica（维吉尼亚鸢尾）
"""

# 导入相关包
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

#1.加载数据集
iris_data = load_iris()
#print(iris_data)   可事先浏览数据集
#2.数据预处理
#3.数据集划分
x_train,x_test,y_train,y_test = train_test_split(iris_data.data,iris_data.target,test_size=0.2,random_state=0)
#4.特征工程
transfer=StandardScaler()
x_train=transfer.fit_transform(x_train)
x_test=transfer.transform(x_test)
#5.模型训练
estimator=KNeighborsClassifier()
#采取网格搜索+交叉验证(4折交叉验证以及K范围取0-10)
param_dict={'n_neighbors':[i for i in range(1,11)]}
estimator=GridSearchCV(estimator,param_dict,cv=4)
estimator.fit(x_train,y_train)
best_k = estimator.best_params_['n_neighbors']
print(f'最优超参是{best_k}')
estimator = estimator.best_estimator_
#6.模型评估
y_predict=estimator.predict(x_test)
print(f'准确率为{accuracy_score(y_test,y_predict)}')
#7.模型预测
print(f'预测结果为{y_predict}')
#依据自定义新数据集对模型进行预测
# my_data=[[7.1,2.8,3.9,1.8]]
# my_data=transfer.transform(my_data)
# y_pre_new=estimator.predict(my_data)
# print(f'预测结果为{y_pre_new}')