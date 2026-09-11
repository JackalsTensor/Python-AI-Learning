from sklearn.datasets import load_wine
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split #分割训练集和测试集
from sklearn.preprocessing import StandardScaler #数据标准化
from sklearn.neighbors import KNeighborsClassifier #KNN算法，分类对象
from sklearn.metrics import accuracy_score #模型评估，计算模型预测准确率


#定义函数，加载数据集并查看数据集
def dm01_winedata():
    wine_data = load_wine()
    print(wine_data.data.shape)
    print(wine_data.data[:5])
    print(wine_data.target[:5])
    print(wine_data.feature_names[:5])
    print(wine_data.DESCR)
    print(wine_data.frame)

#定义函数，绘制散点图
def dm02_show_wine():
    wine_data = load_wine()
    wine_df=pd.DataFrame(wine_data.data, columns=wine_data.feature_names)
    wine_df['label']=wine_data.target
    sns.lmplot(data=wine_df,x='alcohol',y='malic_acid',hue='label',fit_reg=True)
    plt.title('Alcohol vs Malic Acid')
    plt.show()

#定义函数，划分训练集和数据集
def dm03_split_train_test():
    wine_data = load_wine()
    x_train,x_test,y_train,y_test=train_test_split(wine_data.data, wine_data.target, test_size=0.2, random_state=42)
    print(f'训练集的特征：{x_train},个数：{len(x_train)}')
    print(f'训练集的标签：{x_test},个数：{len(x_test)}')
    print(f'测试集的特征：{y_train},个数：{len(y_train)}')
    print(f'测试集的标签：{y_test},个数：{len(y_test)}')

#模型的训练与评估       加载数据集，数据的预处理，特征工程，模型训练，模型评估，模型预测
def dm04_wine_case():

    wine_data = load_wine()
    x_train,x_test,y_train,y_test=train_test_split(wine_data.data, wine_data.target, test_size=0.2, random_state=42)
    transfer=StandardScaler()
    x_train=transfer.fit_transform(x_train)
    x_test=transfer.transform(x_test)

    estimator=KNeighborsClassifier(n_neighbors=3)
    estimator.fit(x_train,y_train)

    y_pre=estimator.predict(x_test)
    print(f'预测值是:{y_pre}')

    # 补全13个特征（这里随便填的示例值，你需要替换成实际数据）
    my_data = [[14.23, 1.71, 2.43, 15.6, 127.0, 2.8, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065.0]]
    # 修正括号，用transfer标准化（和训练集用同一个标准化器）
    my_data = transfer.transform(my_data)
    # 预测
    y_pre_new = estimator.predict(my_data)
    print(f'预测值为:{y_pre_new}')
    # 预测概率
    y_pre_proba = estimator.predict_proba(my_data)
    print(f'预测概率为:{y_pre_proba}')

    print(f'正确率：{estimator.score(x_train,y_train)}')
    print(f'正确率：{accuracy_score(y_test,y_pre)}')
if __name__ == '__main__':
    dm01_winedata()
    dm02_show_wine()
    dm03_split_train_test()
    dm04_wine_case()