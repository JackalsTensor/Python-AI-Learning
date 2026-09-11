from sklearn.feature_selection import VarianceThreshold
import numpy as np
a=np.random.randn(100) #均值为 0、标准差为 1 的正态分布数据
b=np.random.randn(100)*0.1 #生成 100 个标准正态分布的随机数,均值≈0，标准差 = 0.1的正态分布数据
b=np.random.normal(5,0.1,100) #100个均值≈5，标准差 = 0.1的正态分布数据
print(np.var(b))

#构造特征向量
x=np.vstack((a,b)).T
print(x)
print(x.shape)

#进行低方差过滤
from sklearn.feature_selection import VarianceThreshold #用于基于方差筛选特征
vt=VarianceThreshold(0.01) #过滤掉方差≤0.01 的特征
x_filtered=vt.fit_transform(x) #保留方差 > 0.01 的特征
print(x_filtered)
print(x_filtered.shape)