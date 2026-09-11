#1.加载数据
#2.数据预处理
#3.特征工程(提取，预处理......)
#4.模型训练
#5.模型评估
#6.模型预测
from sklearn.datasets import load_iris  #加载鸢尾花数据集
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split #分割训练集和测试集
from sklearn.preprocessing import StandardScaler #数据标准化
from sklearn.neighbors import KNeighborsClassifier #KNN算法，分类对象
from sklearn.metrics import accuracy_score #模型评估，计算模型预测准确率

#1.定义函数，加载鸢尾花数据集并查看数据集
def dm01_loadiris():
    # 1.加载鸢尾花数据集.
    iris_data = load_iris()
    # #2.查看数据集
    # print(f'数据集:{iris_data}') #字典形态
    # print(f'数据集类型:{type(iris_data)}') #<class 'sklearn.utils._bunch.Bunch'>
    # #3.查看数据集中所有键
    # print(f'数据集所有的键:{iris_data.keys()}')
    #4.查看数据集对应的值
    print(f'具体的数据:{iris_data.data[:5]}')  #一共150条数据,
    print(f'具体的标签:{iris_data.target[:5]}')
    print(f'标签对应的名称:{iris_data.target_names}')  #['setosa' 'versicolor' 'virginica']
    print(f'特征对应的名称:{iris_data.feature_names}') #['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
    # print(f'数据集的描述:{iris_data.DESCR}')
#============== ==== ==== ======= ===== ====================
#                Min  Max   Mean    SD   Class Correlation
#============== ==== ==== ======= ===== ====================
#sepal length:   4.3  7.9   5.84   0.83    0.7826
#sepal width:    2.0  4.4   3.05   0.43   -0.4194
#petal length:   1.0  6.9   3.76   1.76    0.9490  (high!)
#petal width:    0.1  2.5   1.20   0.76    0.9565  (high!)
#============== ==== ==== ======= ===== ====================
    # print(f'数据集的框架:{iris_data.frame}') #None
    # print(f'数据集的文件名:{iris_data.filename}') iris.csv

#2.定义函数，绘制散点图
def demo02_show_iris():
    #1.加载数据集
    iris_data = load_iris()
    #2.吧鸢尾花数据集封装成DataFrame对象
    iris_df=pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
    #3.给df对象新增一列-->标签列.
    iris_df['label']=iris_data.target
    # print(iris_df)
    #4.通过seaborn绘制散点图
    #参数分别为数据集，x轴，y轴，分组字段，是否显示拟合线
    sns.lmplot(data=iris_df,x='sepal length (cm)', y='sepal width (cm)', hue='label',fit_reg=True)
    #5.设置标题，显示
    plt.title('iris.data')
    plt.tight_layout()
    plt.show()

#3.定义函数，切分训练集和测试集。
def demo03_split_train_test():
    #1.加载数据集
    iris_data = load_iris()
    #2.数据预处理：从150个特征和标签中，按照8：2比例切分测试机和训练集
    x_train,x_test,y_train,y_test=train_test_split(iris_data.data,iris_data.target, test_size=0.2, random_state=23)
    #3.打印切割后结果
    print(f'训练集的特征:{x_train},个数:{len(x_train)}')
    print(f'训练集的标签:{y_train},个数:{len(y_train)}')
    print(f'测试集的特征:{x_test},个数:{len(x_test)}')
    print(f'测试集的标签:{y_test},个数:{len(y_test)}')

#4.定义函数，实现鸢尾花完整案例->加载数据，数据预处理，特征工程，模型训练，模型评估，模型预测
def demo04_evaluate_test():
    #1.加载数据集
    iris_data = load_iris()
    #2.数据预处理
    x_train,x_test,y_train,y_test=train_test_split(iris_data.data,iris_data.target, test_size=0.2, random_state=23)
    #3.特征工程
    #(1)特征提取：由于只有4个特征例，且都是我们用的因此不需要特征提取
    #(2)特征与处理：因为原数据的4列特征差值不大，所以我们无需特征与处理，但是，加入特征预处理可以让代码更加完善
    #3.1创建标准化对象
    transfer=StandardScaler()
    #3.2 对特征进行标准化，即:x_train:训练集的特征数据，x_test:测试机的特征数据
    #fit_transform:兼具fit和transform的功能，即：训练，转换，该函数适用：第一次进行标准化的时候使用，一般用于处理训练集
    #transform:只有转换，该函数适用：重复进行标准化动作时使用，一般用于对测试集标准化
    x_train=transfer.fit_transform(x_train)
    x_test=transfer.transform(x_test)
    #4.模型训练
    #4.1 创建模型对象
    estimator=KNeighborsClassifier(n_neighbors=4)
    #4.2 具体的训练模型的动作
    estimator.fit(x_train,y_train)    #传入：训练集的特征数据，训练集的标签数据

    #5.模型预测
    #场景1：对刚才切分的测试集进行测试
    y_pre=estimator.predict(x_test)
    print(f'预测值为{y_pre}')

    #场景2:对新数据集进行测试
    #自定义新数据集
    my_data=[[7.1,2.8,3.9,1.8],[6.3,2.7,4.9,1.8],[5.7,2.5,5.0,2.0]]
    #对数据集进行标准化处理
    my_data=transfer.transform(my_data)
    #对模型预测
    y_pre_new=estimator.predict(my_data)
    print(f'预测值为{y_pre_new}')
    #查看上述数据集，每种分类的预测概率
    y_pre_proba=estimator.predict_proba(my_data)
    print(f'预测概率为{y_pre_proba}')      #[[0.         0.66666667 0.33333333]]

    #6.模型评估
    #方式一:直接评分，基于:训练集的特征和训练集的标签
    print(f'正确率（准确率）:{estimator.score(x_test,y_test)}')

    #方式二:基于测试集的标签和预测结果进行评分
    print(f'正确率（准确率）:{accuracy_score(y_test,y_pre)}')

#5.测试函数
if __name__ == '__main__':
    # dm01_loadiris()
    # demo02_show_iris()
    # demo03_split_train_test()
    demo04_evaluate_test()