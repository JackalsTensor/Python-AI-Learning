"""
项目:Kaggle预测心脏病
具体步骤：
    1.加载数据集
    2.数据预处理
    3.划分数据集
    4.特征工程
    5.模型训练(逻辑回归)
    6.模型评估
    7.模型预测
    8.提交示例
"""
#先提前观察数据集特征，预览数据集预先做出判断
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from xgboost.callback import EarlyStopping

# 1.加载数据集
train_df=pd.read_csv(r"D:\PythonProject1\数据集\kaggle预测心脏病赛事数据集\train.csv")
test_df=pd.read_csv(r"D:\PythonProject1\数据集\kaggle预测心脏病赛事数据集\test.csv")

# 2.数据预处理（核心修改：将字符串标签转为数值）
X=train_df.drop(columns=['id','Heart Disease'])
# 映射：Presence→1，Absence→0（必须和赛事要求一致，这是通用规则）
y = train_df['Heart Disease'].map({'Presence': 1, 'Absence': 0})

# 3.划分数据集
X_train,X_val,y_train,y_val=train_test_split(X,y,test_size=0.2,random_state=42)

# 4.特征工程
scaler=StandardScaler()
X_train=scaler.fit_transform(X_train)
X_val=scaler.transform(X_val)

# 5.模型训练(XGBoost)
estimator = XGBClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=5,
    min_child_weight=1,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    scale_pos_weight=1,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)

# 定义早停回调
early_stop = EarlyStopping(rounds=20, save_best=True)

# 修正后的 fit 调用
estimator.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=False
)

# 6.模型评估（核心修改：pos_label改为数值1）
y_predict=estimator.predict(X_val)
print(f'准确率为{accuracy_score(y_val,y_predict)}')
print(f'精确率为{precision_score(y_val,y_predict,pos_label=1)}')
print(f'召回率为{recall_score(y_val,y_predict,pos_label=1)}')
print(f'F1值为{f1_score(y_val,y_predict,pos_label=1)}')
print(f'预测结果为{y_predict}')

# 7.模型预测（预测结果已自动是数值1/0，无需转换）
test_id=test_df['id'].copy()
X_test=test_df.drop(columns=['id'])
X_test=scaler.transform(X_test)
y_test_predict=estimator.predict(X_test)  # 输出为1/0的数组
print(f'测试集预测结果为{y_test_predict}')

# 8.提交文件（直接保存数值，类型为int，符合赛事要求）
submission=pd.DataFrame({
    'id': test_id,
    'Heart Disease': y_test_predict.astype(int)  # 强制转为int类型，避免浮点
})

submission.to_csv(
    path_or_buf=r'C:\Users\fangkaimin\Desktop\JackalsTensor_heart_disease(XGBoost).csv',
    index=False,
    encoding='utf-8'
)
print("提交文件已生成，类型检查：")