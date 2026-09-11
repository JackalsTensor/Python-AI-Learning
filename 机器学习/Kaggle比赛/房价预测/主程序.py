"""
Kaggle比赛项目：房价预测
具体步骤：
    1.加载数据集
    2.数据预处理
    3.数据集划分
    4.特征工程(标准化)
    5.模型训练(线性回归)
    6.模型评估
    7.训练的模型预测测试集
    8.提交示例
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import  mean_squared_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

#1.加载数据集
train_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle房价预测赛事数据集\train.csv")
test_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle房价预测赛事数据集\test.csv")

#2.数据预处理
#查看训练集的特征
# print(train_df.info())   #查看训练集的特征
#根据训练集数据集无缺失值观测，发现有部分特征存在缺失问题.如果将有缺失值的行删去则可能造成大量数据损失，对此，我考虑将缺失值删除
#先挑出无缺失值的列并打印出列表
train_df_no_nan=train_df.dropna(axis=1)
# print(train_df_no_nan.columns)
#将训练集数据集进行重新赋值,完成训练集清洗缺失值的操作
train_df=train_df[train_df_no_nan.columns]

# ========== 补充：训练集填充缺失值（防止残留NaN） ==========
train_num_cols = train_df.select_dtypes(include=['int64', 'float64']).columns
train_df[train_num_cols] = train_df[train_num_cols].fillna(train_df[train_num_cols].median())
train_obj_cols = train_df.select_dtypes(include=['object']).columns
train_df[train_obj_cols] = train_df[train_obj_cols].fillna('None')

#查看测试集特征
# print(test_df.info())
#根据测试集数据集无缺失值观测，发现有部分特征存在缺失问题,同理对其进行缺失值处理
keep_cols = train_df_no_nan.columns.drop('SalePrice')
test_df = test_df[keep_cols]

# ========== 关键补充：测试集填充缺失值（解决NaN报错） ==========
test_num_cols = test_df.select_dtypes(include=['int64', 'float64']).columns
test_df[test_num_cols] = test_df[test_num_cols].fillna(test_df[test_num_cols].median())  # 数值列填中位数
test_obj_cols = test_df.select_dtypes(include=['object']).columns
test_df[test_obj_cols] = test_df[test_obj_cols].fillna('None')  # 文本列填None

# print(test_df.info())
#对训练集的特征和标签进行拆分
x_train_full=train_df.drop(columns=['SalePrice'])
y_train_full=train_df['SalePrice']
#由于数据集内有文本列，所以需要将其进行热编码
#区分数值列和文本列
numeric_features = x_train_full.select_dtypes(include=['int64', 'float64']).columns
categorical_features = x_train_full.select_dtypes(include=['object']).columns

#定义预处理管道:文本列独热编码,数值列直接保留
preprocessor = ColumnTransformer(
    transformers=[
        #文本列
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        #数值列
        ('num', 'passthrough', numeric_features)
    ])
#对完整训练集特征做[拟合+转换]
x_train_encoded = preprocessor.fit_transform(x_train_full)

#3.数据集划分
x_train,x_test,y_train,y_test=train_test_split(x_train_encoded,y_train_full,test_size=0.2,random_state=42)
# print(f'训练集的特征：{x_train},个数：{len(x_train)}')
# print(f'训练集的标签：{y_train},个数：{len(y_train)}')
# print(f'测试集的特征：{x_test},个数：{len(x_test)}')
# print(f'测试集的标签：{y_test},个数：{len(y_test)}')

#4.特征工程(标准化)
estimator=StandardScaler(with_mean=False)
x_train=estimator.fit_transform(x_train)
x_test=estimator.transform(x_test)

#5.模型训练(线性回归)
estimator2=LinearRegression()
estimator2.fit(x_train,y_train)
y_pred=estimator2.predict(x_test)
# print(f'预测结果：{y_pred}')
# print(f'真实结果：{y_test}')

#6.模型评估(利用均方误差评估)
print(f'训练集的均方误差：{mean_squared_error(y_test,y_pred)}')
print(f'训练集的决定系数：{r2_score(y_test,y_pred)}')
#可视化处理(散点图)
plt.scatter(y_test,y_pred)
plt.plot(np.sort(y_test),np.sort(y_pred),color='r')
# plt.show()

#7.训练的模型预测测试集
# 对测试集特征进行预处理
x_test_encoded = preprocessor.transform(test_df)
x_test_scale=estimator.transform(x_test_encoded)
y_test_pred=estimator2.predict(x_test_scale)
print(f'\n测试集预测结果:{y_test_pred}')
print(f'测试集预测结果总数：{len(y_test_pred)}')

#8.提交示例
submission = pd.DataFrame({
    'Id': test_df['Id'],
    'SalePrice': y_test_pred
})
# 保存到桌面（示例，可改成你自己的路径）
submission.to_csv(
    r'C:\Users\fangkaimin\Desktop\JackalsTensor_house_price_prediction.csv',
    index=False,
    encoding='utf-8'
)