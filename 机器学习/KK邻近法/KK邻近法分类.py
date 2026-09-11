"""
代码实现思路：
先导包-->准备好训练集和测试集-->创建KNN模型对象-->模型训练与预测
由于奥卡姆剃刀原则，预测结果更偏向较小的值
"""
from sklearn.neighbors import KNeighborsClassifier
x_train=[[0],[1],[2],[3],[4],[5]]       #训练集的特征数据
y_train=[0,1,0,1,1,0]                   #训练集的标签数据
x_test=[[6]]                            #测试集的特征数据
estimator = KNeighborsClassifier(n_neighbors=3)   #neighbors：近邻的个数
estimator.fit(x_train,y_train)                #模拟训练
print(estimator.predict(x_test))