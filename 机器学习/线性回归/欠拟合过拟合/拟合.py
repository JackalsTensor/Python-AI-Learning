#案例：演示欠拟合,过拟合,恰好拟合
#导包
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge,Lasso

#1.定义函数，模拟欠拟合
def dm01_under_fitting():
    #随机生成100个数据点
    np.random.seed(23)
    x=np.random.uniform(-3,3,100)
    y=0.5*x**2+x+2+np.random.normal(0,1,100)
    # print(f'特征矩阵X:{x}')
    # print(f'标签向量y:{y}')
    #数据预处理
    X=x.reshape(-1,1)
    # print(f'处理后的特征矩阵X:{X}')
    #模型训练
    estimator=LinearRegression()
    estimator.fit(X,y)
    #模型预测
    y_predict=estimator.predict(X)
    # print(f'预测结果为{y_predict}')
    #模型评估
    print(f'欠拟合均方误差为{mean_squared_error(y,y_predict)}')
    print(f'欠拟合准确率为{estimator.score(X,y)}')
    #画图
    plt.scatter(x,y)
    plt.plot(x,y_predict,color='r')
    plt.show()

#2.定义函数，模拟恰好拟合
def dm02_just_fitting():
    # 随机生成100个数据点
    np.random.seed(23)
    x = np.random.uniform(-3, 3, 100)
    y = 0.5 * x ** 2 + x + 2 + np.random.normal(0, 1, 100)
    # print(f'特征矩阵X:{x}')
    # print(f'标签向量y:{y}')
    # 数据预处理
    X = x.reshape(-1, 1)
    # print(f'处理后的特征矩阵X:{X}')
    #因为模型目前过于简单，会出现欠拟合，因此增加一列特征列，使得模型更加复杂
    #即把数据从[[1],[2],[3],[4]]->[[1,1],[2,4],[3,9],[4,16]]
    X2=np.hstack([X,X**2])#该函数作用：横向拼接,拼接后数组行数不变，列数增加
    # 模型训练
    estimator = LinearRegression()
    estimator.fit(X2, y)
    # 模型预测
    y_predict = estimator.predict(X2)
    # print(f'预测结果为{y_predict}')
    # 模型评估
    print(f'恰好拟合均方误差为{mean_squared_error(y, y_predict)}')
    print(f'恰好拟合准确率为{estimator.score(X2, y)}')
    # 画图
    plt.scatter(x, y)
    plt.plot(np.sort(x), y_predict[np.argsort(x)], color='r')
    plt.show()

#3.定义函数，模拟过拟合
def dm03_over_fitting():
    # 随机生成100个数据点
    np.random.seed(23)
    x = np.random.uniform(-3, 3, 100)
    y = 0.5 * x ** 2 + x + 2 + np.random.normal(0, 1, 100)
    # print(f'特征矩阵X:{x}')
    # print(f'标签向量y:{y}')
    # 数据预处理
    X = x.reshape(-1, 1)
    # print(f'处理后的特征矩阵X:{X}')
    #因为模型目前过于简单，会出现欠拟合，因此增加9列特征列，使得模型更加复杂
    X3=np.hstack([X,X**2,X**3,X**4,X**5,X**6,X**7,X**8,X**9])#该函数作用：横向拼接,拼接后数组行数不变，列数增加
    # 模型训练
    estimator = LinearRegression()
    estimator.fit(X3, y)
    # 模型预测
    y_predict = estimator.predict(X3)
    # print(f'预测结果为{y_predict}')
    # 模型评估
    print(f'过拟合均方误差为{mean_squared_error(y, y_predict)}')
    print(f'过拟合准确率为{estimator.score(X3, y)}')
    # 画图
    plt.scatter(x, y)
    plt.plot(np.sort(x), y_predict[np.argsort(x)], color='r')
    plt.show()

#4.定义函数，模拟L1正则化
def dm04_Lasso_fitting():
    # 随机生成100个数据点
    np.random.seed(23)
    x = np.random.uniform(-3, 3, 100)
    y = 0.5 * x ** 2 + x + 2 + np.random.normal(0, 1, 100)
    # print(f'特征矩阵X:{x}')
    # print(f'标签向量y:{y}')
    # 数据预处理
    X = x.reshape(-1, 1)
    # print(f'处理后的特征矩阵X:{X}')
    #因为模型目前过于简单，会出现欠拟合，因此增加9列特征列，使得模型更加复杂
    X3=np.hstack([X,X**2,X**3,X**4,X**5,X**6,X**7,X**8,X**9])#该函数作用：横向拼接,拼接后数组行数不变，列数增加
    # 模型训练
    estimator=Lasso(alpha=0.1) #alpha:正则化系数，默认为1
    estimator.fit(X3, y)
    # 模型预测
    y_predict = estimator.predict(X3)
    # print(f'预测结果为{y_predict}')
    # 模型评估
    print(f'L1正则化均方误差为{mean_squared_error(y, y_predict)}')
    print(f'L2正则化准确率为{estimator.score(X3, y)}')
    # 画图
    plt.scatter(x, y)
    plt.plot(np.sort(x), y_predict[np.argsort(x)], color='r')
    plt.show()

#5.定义函数，模拟L2正则化
def dm05_Ridge_fitting():
    # 随机生成100个数据点
    np.random.seed(23)
    x = np.random.uniform(-3, 3, 100)
    y = 0.5 * x ** 2 + x + 2 + np.random.normal(0, 1, 100)
    # print(f'特征矩阵X:{x}')
    # print(f'标签向量y:{y}')
    # 数据预处理
    X = x.reshape(-1, 1)
    # print(f'处理后的特征矩阵X:{X}')
    # 因为模型目前过于简单，会出现欠拟合，因此增加9列特征列，使得模型更加复杂
    X3 = np.hstack([X, X ** 2, X ** 3, X ** 4, X ** 5, X ** 6, X ** 7, X ** 8, X ** 9])  # 该函数作用：横向拼接,拼接后数组行数不变，列数增加
    # 模型训练
    estimator = Ridge(alpha=0.1)  # alpha:正则化系数，默认为1
    estimator.fit(X3, y)
    # 模型预测
    y_predict = estimator.predict(X3)
    # print(f'预测结果为{y_predict}')
    # 模型评估
    print(f'L2正则化均方误差为{mean_squared_error(y, y_predict)}')
    print(f'L2正则化准确率为{estimator.score(X3, y)}')
    # 画图
    plt.scatter(x, y)
    plt.plot(np.sort(x), y_predict[np.argsort(x)], color='r')
    plt.show()

#6.测试
if __name__ == '__main__':
    dm01_under_fitting()
    dm02_just_fitting()
    dm03_over_fitting()
    dm04_Lasso_fitting()
    dm05_Ridge_fitting()