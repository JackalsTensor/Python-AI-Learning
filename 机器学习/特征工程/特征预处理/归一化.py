#归一化原理：将特征值线性映射到 [0, 1] 区间（或指定的 [a, b] 区间），保留原始数据的相对分布
#公式：X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
#防止因为量纲（单位）问题，导致特征方差值相差较大，影响模型最终结果

from sklearn.preprocessing import MinMaxScaler

#1.准备数据集(归一化之前原数据)
x_train=[[90,2,10,40],[60,4,15,45],[75,3,13,46]]

#2.创建归一化对象
transfer=MinMaxScaler()

#3.对原数据集归一化操作
x_train_new=transfer.fit_transform(x_train)

#4.打印后的数据集
print('归一化后的数据集为:\n')
print(x_train_new)