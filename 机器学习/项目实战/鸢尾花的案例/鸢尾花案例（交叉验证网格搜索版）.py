from sklearn.datasets import load_iris  #加载鸢尾花数据集
from sklearn.model_selection import train_test_split,GridSearchCV #分割训练集和测试集,寻找最优超参(网格搜索+交叉验证)
from sklearn.preprocessing import StandardScaler #数据标准化
from sklearn.neighbors import KNeighborsClassifier #KNN算法，分类对象
from sklearn.metrics import accuracy_score #模型评估，计算模型预测准确率
iris = load_iris()
x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=22)
#3.特征工程->数据预处理->标准化
transfer=StandardScaler()
x_train=transfer.fit_transform(x_train)
x_test=transfer.transform(x_test)

estimator=KNeighborsClassifier()
#定义字典，记录超参可能出现的情况
param_dict={'n_neighbors':[i for i in range(1,11)]}
#创建GridSearchCV对象->寻找最优超参，使用网格搜索+交叉验证方式
estimator=GridSearchCV(estimator,param_dict,cv=4)

estimator.fit(x_train, y_train)
best_k = estimator.best_params_['n_neighbors']
print(best_k)
#打印最优超参组合
print(f'最优评分:{estimator.best_score_}')
print(f'最优超参组合:{estimator.best_params_}')
print(f'最优估计器对象:{estimator.best_estimator_}')
print(f'具体的交叉验证结果:{estimator.cv_results_}')

estimator=KNeighborsClassifier(n_neighbors=3)
estimator.fit(x_train, y_train)
y_pred=estimator.predict(x_test)
print(f'准确率:{accuracy_score(y_test,y_pred)}')