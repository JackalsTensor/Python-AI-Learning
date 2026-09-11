"""
利用随机森林解决泰坦尼克号幸存者问题
具体步骤:
    1.加载数据集
    2.数据预处理
    3.划分数据集
    4.特征工程
    5.模型训练
    6.模型评估
    7.模型预测
    8.提交样例
"""
#导包
import pandas as pd
from numpy.conftest import dtype
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.metrics import classification_report


#1.加载数据集
train_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle泰坦尼克号预测幸存者赛事数据集\Titanic-Train.csv")
test_df=pd.read_csv(r"D:\PythonProject1\数据集\Kaggle泰坦尼克号预测幸存者赛事数据集\Titanic-Test.csv")

#2.数据预处理
#2.1数据清洗
#(1)首先观察Age特征列，发现Age列有缺失值，需要处理
age_total = len(train_df['Age'])
age_missing = train_df['Age'].isnull().sum()
age_missing_rate = age_missing / age_total * 100
# print(f'age缺失率：{age_missing_rate:.2f}%')
#经过处理发现，缺失值占比为百分之10.77，可以采用中位值填充
train_df['Age'] = train_df['Age'].fillna(train_df['Age'].median())
#(2)观察Passenger Class特征列发现，只有First,Second,Third三个标签，且舱位代表了乘客的等级，因此，可以采用有序的独热编码进行转换
Pclass_map={
    'First':0,
    'Second':1,
    'Third':2
}
train_df['Passenger Class'] = train_df['Passenger Class'].map(Pclass_map)
#(3)观察Sex特征列，发现只有两个标签，且性别代表了乘客的性别，因此，可以采用无序的独热编码进行转换
train_df=pd.get_dummies(
    data=train_df,
    columns=['Sex'],
    drop_first=True,
    prefix='Sex',
    dtype='int'
)
#(4)观察Port of Embarkation特征列，发现只有三个标签，且上船的港口代表了乘客的出发港口，因此，可以采用无序的独热编码进行转换在此之前先处理缺失值
train_df['Port of Embarkation'] = train_df['Port of Embarkation'].fillna(train_df['Port of Embarkation'].mode()[0])
train_df=pd.get_dummies(
    data=train_df,
    columns=['Port of Embarkation'],
    drop_first=True,
    prefix='Port of Embarkation',
    dtype='int'
)
#(5)观察LifeBoat特征列，发现缺失率很高且有文本不易处理，考虑将是否登上救船作为一个新的特征
train_df['Has_Lifeboat'] = train_df['Life Boat'].notna().astype(int)
train_df=train_df.drop('Life Boat',axis=1)
#(6)观察Cabin特征列，发现缺失率很高且文本不易处理，考虑将是否有船票作为新的特征
train_df['Has_Cabin'] = train_df['Cabin'].notna().astype(int)
train_df=train_df.drop('Cabin',axis=1)
#观察数据集剩余特征列,由于Name,Ticket Number是对模型训练影响不大的,因此,考虑删除
train_df=train_df.drop(['Name','Ticket Number'],axis=1)
#2.2.取出特征和标签
X=train_df.drop(columns=['Survived','PassengerId'])
y=train_df['Survived']

#3.划分数据集
X_train,X_val,y_train,y_val=train_test_split(X,y,test_size=0.2,random_state=42)

#4.特征工程
scaler=StandardScaler()
X_train=scaler.fit_transform(X_train)
X_val=scaler.transform(X_val)

#5.模型训练
estimator=RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    min_samples_leaf=5
)
estimator.fit(X_train,y_train)

#6.模型评估
y_pred=estimator.predict(X_val)
print(f'准确率：{accuracy_score(y_val,y_pred)}')
print(classification_report(y_val,y_pred))

#7.模型预测
#7.1数据预处理(与训练集处理方式一致)
test_df['Age'] = test_df['Age'].fillna(test_df['Age'].median())
test_df['Passenger Class'] = test_df['Passenger Class'].map(Pclass_map)
test_df=pd.get_dummies(
    data=test_df,
    columns=['Sex'],
    drop_first=True,
    prefix='Sex',
    dtype='int'
)
test_df['Port of Embarkation'] = test_df['Port of Embarkation'].fillna(test_df['Port of Embarkation'].mode()[0])
test_df=pd.get_dummies(
    data=test_df,
    columns=['Port of Embarkation'],
    drop_first=True,
    prefix='Port of Embarkation',
    dtype='int'
)
test_df['Has_Lifeboat'] = test_df['Life Boat'].notna().astype(int)
test_df=test_df.drop('Life Boat',axis=1)
test_df['Has_Cabin'] = test_df['Cabin'].notna().astype(int)
test_df=test_df.drop('Cabin',axis=1)
test_df=test_df.drop(['Name','Ticket Number'],axis=1)
X_test=test_df.drop(columns=['PassengerId'])
X_test=scaler.transform(X_test)
y_test_pred=estimator.predict(X_test)

# #8.提交样例
# submission=pd.DataFrame(
#     {
#         'PassengerId':test_df['PassengerId'],
#         'Survived':y_test_pred
#     }
# )
# submission.to_csv(
#     r'C:\Users\fangkaimin\Desktop\JackalsTensor_titanic.csv',
#     index=False,
#     encoding='utf-8'
# )
# print('提交成功')