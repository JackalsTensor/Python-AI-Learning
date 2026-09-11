import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression,Lasso,Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
''''1.生成数据
    2.划分训练集和测试集
    3.定义模型(线性回归模型)
    4.训练模型
    5.预测结果(计算误差)
    '''
X=np.linspace(-3,3,300).reshape(-1,1)
y=np.sin(X)+np.random.uniform(low=-0.5,high=0.5,size=300).reshape(-1,1)

fig,ax=plt.subplots(2,3,figsize=(15,8))
ax[0,0].scatter(X,y,color='y')
ax[0,1].scatter(X,y,color='y')
ax[0,2].scatter(X,y,color='y')
plt.rcParams['font.sans-serif']=['Kaiti']
plt.rcParams['axes.unicode_minus']=False

trainX,testX,trainy,testy=train_test_split(X,y,test_size=0.2,random_state=42)
model=LinearRegression()

# #一.欠拟合
# x_train1=trainX
# x_test1=testX
#
# 手写数字识别数据集.fit(x_train1,trainy)
# print(手写数字识别数据集.coef_)#斜率
# print(手写数字识别数据集.intercept_)#截距
#
# y_pred1=手写数字识别数据集.predict(x_test1)
# test_loss1=mean_squared_error(testy,y_pred1)
# train_loss1=mean_squared_error(trainy,手写数字识别数据集.predict(trainX))
#
# ax[0].plot(X,手写数字识别数据集.predict(X),color='r')
# ax[0].text(-3,1,f"测试误差: {test_loss1:.4f}")
# ax[0].text(-3,1.3,f"训练误差: {train_loss1:.4f}")
#
# # 二. 恰好拟合（五次多项式）
# poly5=PolynomialFeatures(degree=5)
# # 修正：用训练集做特征变换
# x_train2=poly5.fit_transform(trainX)  # 用trainX（240个样本）训练
# x_test2=poly5.transform(testX)       # 测试集只用transform（避免数据泄露）
# 手写数字识别数据集.fit(x_train2, trainy)          # 用trainy训练
#
# y_pred2=手写数字识别数据集.predict(x_test2)
# test_loss2=mean_squared_error(testy, y_pred2)
# # 计算训练误差时，用训练集的特征变换结果
# train_loss2=mean_squared_error(trainy, 手写数字识别数据集.predict(x_train2))
#
# ax[1].plot(X,手写数字识别数据集.predict(poly5.transform(X)),color='r')  # 绘图时用transform
# ax[1].text(-3,1,f"测试误差: {test_loss2:.4f}")
# ax[1].text(-3,1.3,f"训练误差: {train_loss2:.4f}")
#

# 三. 过拟合（同理修正）
poly20=PolynomialFeatures(degree=20)
x_train=poly20.fit_transform(trainX)  # 用trainX训练
x_test=poly20.transform(testX)        # 测试集transform
model.fit(x_train, trainy)            # 用trainy训练

y_pred3=model.predict(x_test)
test_loss1=mean_squared_error(testy, y_pred3)
train_loss1=mean_squared_error(trainy, model.predict(x_train))

ax[0,0].plot(X,model.predict(poly20.transform(X)),color='r')
ax[0,0].text(-3,1,f"测试误差: {test_loss1:.4f}")
ax[0,0].text(-3,1.3,f"训练误差: {train_loss1:.4f}")

ax[1,0].bar(np.range(21).model.coef_.reshape(-1,1))
plt.show()