from sklearn.neighbors import KNeighborsRegressor
#准备数据集
x_train=[[0,0,1],[1,1,0],[3,10,10],[4,11,12]]
y_train=[0.1,0.2,0.3,0.4]
x_test=[[3,11,20]]
#创建模型对象
estimator=KNeighborsRegressor(n_neighbors=3)
#模型训练
estimator.fit(x_train,y_train)
#模型预测
y_pred=estimator.predict(x_test)
print(y_pred)