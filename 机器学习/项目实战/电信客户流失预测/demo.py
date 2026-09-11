"""
案例：通过逻辑回归算法，针对电信用户数据建模，进行预测分析
"""
#导包
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,accuracy_score,precision_score,recall_score,f1_score
#1.定义函数，进行数据预处理
def demo01_data_preprocessing():
    churn_df=pd.read_csv("D:\PythonProject1\数据集\电信客户流失预测数据集\WA_Fn-UseC_-Telco-Customer-Churn.csv")
    #因为churn和customerID都是非数值特征，所以需要进行热编码处理(one-hot)
    churn_df=pd.get_dummies(churn_df,columns=['Churn','gender'])
    churn_df.drop(['Churn_No','gender_Male'],axis=1,inplace=True)
    #修改数据集的列名
    churn_df.rename(columns={'Churn_Yes':'flag'},inplace=True)
    # 处理后的数据集信息
    print(churn_df.info())
    print(churn_df.head(5))
    #查看数据集的分布
    print(churn_df.flag.value_counts())
#2.定义函数，演示数据可视化
def demo02_data_visualization():
    churn_df=pd.read_csv("D:\PythonProject1\数据集\电信客户流失预测数据集\WA_Fn-UseC_-Telco-Customer-Churn.csv")
    churn_df=pd.get_dummies(churn_df,columns=['Churn','gender'])
    churn_df.drop(['Churn_No','gender_Male'],axis=1,inplace=True)
    churn_df.rename(columns={'Churn_Yes':'flag'},inplace=True)
    print(churn_df.columns)  # 查看数据集的列名
    #数据的可视化，绘制计数柱状图
    sns.countplot(data=churn_df,x='Contract',hue='flag')
    plt.show()
#3.定义函数，进行逻辑回归建模，预测分析，评估模型
def demo03_logistic_regression():
    # 1. 读取数据（用原始字符串避免转义问题）
    churn_df = pd.read_csv(r"D:\PythonProject1\数据集\电信客户流失预测数据集\WA_Fn-UseC_-Telco-Customer-Churn.csv")

    # 2. 处理 TotalCharges 列的缺失值和类型问题
    churn_df['TotalCharges'] = pd.to_numeric(churn_df['TotalCharges'], errors='coerce')
    churn_df['TotalCharges'].fillna(churn_df['TotalCharges'].median(), inplace=True)

    # 3. 对所有分类特征做独热编码
    categorical_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                        'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                        'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
                        'PaperlessBilling', 'PaymentMethod']
    churn_df = pd.get_dummies(churn_df, columns=categorical_cols, drop_first=True)

    # 4. 处理标签列 Churn
    churn_df = pd.get_dummies(churn_df, columns=['Churn'], drop_first=True)
    churn_df.rename(columns={'Churn_Yes': 'flag'}, inplace=True)

    # 5. 分离特征和标签，去掉无用的 customerID
    X = churn_df.drop(['flag', 'customerID'], axis=1)
    y = churn_df['flag']

    # 6. 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # 7. 标准化特征（只对数值型特征做）
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # 8. 训练逻辑回归模型（增加迭代次数确保收敛）
    estimator = LogisticRegression(max_iter=1000)
    estimator.fit(X_train, y_train)

    # 9. 预测并评估
    y_predict = estimator.predict(X_test)
    print("预测结果:\n", y_predict)
    print("准确率:", accuracy_score(y_test, y_predict))
    print("精确率:", precision_score(y_test, y_predict))
    print("召回率:", recall_score(y_test, y_predict))
    print("F1值:", f1_score(y_test, y_predict))


#4.测试
if __name__ == '__main__':
    # demo01_data_preprocessing()
    # demo02_data_visualization()
    demo03_logistic_regression()