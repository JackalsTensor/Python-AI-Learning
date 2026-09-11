from sklearn.linear_model import LinearRegression
#1.准备数据
x_train=[[160],[166],[172],[174],[180]]
y_train=[56.3,60.6,65.1,68.5,75]
x_test=[[176]]
#2.创建模型对象
estimator=LinearRegression()
estimator.fit(x_train,y_train)
#查看斜率和权重
print(f'斜率是：{estimator.coef_}')
print(f'截距是：{estimator.intercept_}')
#3.模型预测
y_pred=estimator.predict(x_test)
print(y_pred)