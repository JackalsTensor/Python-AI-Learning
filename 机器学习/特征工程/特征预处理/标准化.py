#标准差计算公式：标准差 = √(1/n * ∑(xi - x_mean)^2)

from sklearn.preprocessing import StandardScaler

#1.准备数据集(标准化之前原数据)
x_train=[[90,2,10,40],[60,4,15,45],[75,3,13,46]]

#2.创建标准化对象
transfer=StandardScaler()

#3.对原数据集标准化操作
x_train_new=transfer.fit_transform(x_train)

#4.打印后的数据集
print('标准化后的数据集为:\n')
print(x_train_new)
print(f'数据集的均值为:{transfer.mean_}')
print(f'数据集的方差为:{transfer.var_}')
print(f'数据集的标准差为:{transfer.scale_}')