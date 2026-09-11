"""
Kaggle比赛项目：对学生成绩进行预测
考虑该项目完整步骤：
    1.加载数据集
    2.数据集预处理
    3.划分数据集
    4.特征工程
    5.模型训练
    6.模型评估
    7.模型预测
    8.提交预测结果
"""
from tarfile import LinkOutsideDestinationError

#先观察数据集特征，预览数据集预先做出判断
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor

#1.加载数据集
train_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle学生成绩预测赛事数据集\train (1).csv")
test_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle学生成绩预测赛事数据集\test (1).csv")

#2.数据预处理
# print(train_df.info())
#观察数据集特征，发现无任何缺失值或者异常数据，因此不进行数据清洗
#查看测试集特征
test_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle学生成绩预测赛事数据集\test (1).csv")
# print(test_df.info())
#观察数据集特征，发现无任何缺失值或者异常数据，因此不进行数据清洗
#由于数据集内有文本列，所以需要将其进行热编码

#热编码处理(重点!!!)
#首先对训练集中的性别进行热编码
#(1).我们观察到，由于gender只有三个类别，也就是feamle,male,other三类，因此，我们考虑使用无序的独热编码
train_df=pd.get_dummies(
    data=train_df,
    columns=['gender'],
    drop_first=True,
    prefix='gender'
)
#(2).我们观察到，由于course和gender类似，因此，我们仍然考虑使用无序的独热编码
train_df=pd.get_dummies(
    data=train_df,
    columns=['course'],
    drop_first=True,
    prefix='course'
)
#(3).我们观察到，由于internet_access只有两个类别，也就是是Yes和No，因此，我们考虑二分类编码
train_df['internet_access_encoded'] = train_df['internet_access'].map({
    'yes': 1,
    'no': 0
})
#(4).我们观察到，由于sleep_quality中各个类别有天然的顺序关系，因此考虑使用有序热编码
sleep_map={
    'poor':0,
    'average':1,
    'good':2
}
train_df['sleep_quality_encoded'] = train_df['sleep_quality'].map(sleep_map)
#(5).我们观察到，由于study_method中各个类别无顺序关系，因此考虑使用无序热编码
train_df=pd.get_dummies(
    data=train_df,
    columns=['study_method'],
    drop_first=True,
    prefix='study_method'
)
#(6).我们观察到，由于facility_rating中各个类别有天然的顺序关系，因此考虑使用有序热编码
facility_map={
    'low':0,
    'medium':1,
    'high':2
}
train_df['facility_rating_encoded'] = train_df['facility_rating'].map(facility_map)
#(7).我们观察到，由于exam_difficulity中各个类别有天然的顺序关系，因此考虑使用有序热编码
difficulty_map={
    'easy':0,
    'moderate':1,
    'hard':2
}
train_df['exam_difficulty_encoded'] = train_df['exam_difficulty'].map(difficulty_map)

#划分特征和标签
target_column='exam_score'
X=train_df.drop(columns=[target_column,'id'])
y=train_df[target_column]

#3.划分数据集
X_train,X_val,y_train,y_val=train_test_split(X,y,test_size=0.2,random_state=42)

#4.特征工程
#只对数值型特征进行标准化
numeric_cols=['age','study_hours','class_attendance','sleep_hours']
scaler=StandardScaler()
X_train[numeric_cols]=scaler.fit_transform(X_train[numeric_cols])
X_val[numeric_cols]=scaler.transform(X_val[numeric_cols])
# 1. 删除原始的字符串列（冗余列，已生成编码列）
cols_to_drop = ['internet_access', 'sleep_quality', 'facility_rating', 'exam_difficulty']
X_train = X_train.drop(columns=cols_to_drop, errors='ignore')
X_val = X_val.drop(columns=cols_to_drop, errors='ignore')

# 2. 将bool类型列转为int（XGBoost兼容int，不兼容bool）
bool_cols = X_train.select_dtypes(include=['bool']).columns.tolist()
for col in bool_cols:
    X_train[col] = X_train[col].astype(int)
    X_val[col] = X_val[col].astype(int)

# 3. 填充可能的缺失值（保险措施）
X_train = X_train.fillna(0)
X_val = X_val.fillna(0)


#5.模型训练(使用线性回归进行预测)
estimator2=LinearRegression()
estimator2.fit(X_train,y_train)
y_pred=estimator2.predict(X_val)

#6.模型评估(利用均方误差评估)
# print(f'训练集的均方误差：{mean_squared_error(y_val,y_pred)}')
# print(f'训练集的决定系数：{r2_score(y_val,y_pred)}')
plt.scatter(y_val,y_pred)
plt.plot(np.sort(y_val),np.sort(y_pred),color='r')
# plt.show()

#7.模型预测
#首先需要对测试集进行预处理，对其进行热编码处理逻辑与训练集处理方式一致
#(1).我们观察到，由于gender只有三个类别，也就是feamle,male,other三类，因此，我们考虑使用无序的独热编码
test_df=pd.get_dummies(
    data=test_df,
    columns=['gender'],
    drop_first=True,
    prefix='gender'
)
#(2).我们观察到，由于course和gender类似，因此，我们仍然考虑使用无序的独热编码
test_df=pd.get_dummies(
    data=test_df,
    columns=['course'],
    drop_first=True,
    prefix='course'
)
#(3).我们观察到，由于internet_access只有两个类别，也就是是Yes和No，因此，我们考虑二分类编码
test_df['internet_access_encoded'] = test_df['internet_access'].map({
    'yes': 1,
    'no': 0
})
#(4).我们观察到，由于sleep_quality中各个类别有天然的顺序关系，因此考虑使用有序热编码
sleep_map={
    'poor':0,
    'average':1,
    'good':2
}
test_df['sleep_quality_encoded'] = test_df['sleep_quality'].map(sleep_map)
#(5).我们观察到，由于study_method中各个类别无顺序关系，因此考虑使用无序热编码
test_df=pd.get_dummies(
    data=test_df,
    columns=['study_method'],
    drop_first=True,
    prefix='study_method'
)
#(6).我们观察到，由于facility_rating中各个类别有天然的顺序关系，因此考虑使用有序热编码
facility_map={
    'low':0,
    'medium':1,
    'high':2
}
test_df['facility_rating_encoded'] = test_df['facility_rating'].map(facility_map)
#(7).我们观察到，由于exam_difficulity中各个类别有天然的顺序关系，因此考虑使用有序热编码
difficulty_map={
    'easy':0,
    'moderate':1,
    'hard':2
}
test_df['exam_difficulty_encoded'] = test_df['exam_difficulty'].map(difficulty_map)
#剩下的操作与训练集时进行的操作基本一致，只需将测试集的编码逻辑与训练集的编码逻辑一致即可
train_feature_cols = X_train.columns.tolist()
test_id = test_df['id'].copy()
#划分测试集的特征和标签
X_test_final = test_df.drop(columns=['id'])
X_test_final = X_test_final[train_feature_cols]
# 对数值型特征进行标准化
numeric_cols = ['age', 'study_hours', 'class_attendance', 'sleep_hours']
X_test_final[numeric_cols] = scaler.transform(X_test_final[numeric_cols])
y_test_pred = estimator2.predict(X_test_final)
print(f'测试集预测结果:{y_test_pred}')

# #8.提交示例
# submission = pd.DataFrame({
#     'id': test_id,
#     'exam_score': y_test_pred
# })
# submission.to_csv(
#     r'C:\Users\fangkaimin\Desktop\JackalsTensor_exam_score_prediction(线性回归).csv',
#     index=False,
#     encoding='utf-8'
# )