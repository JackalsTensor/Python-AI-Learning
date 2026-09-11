import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, classification_report)
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#读取原始数据
file_path = r"D:\PythonProject1\数学建模\2025国赛C题\原数据集\完整合并数据.csv"
df_full = pd.read_csv(file_path)
print(f"原始数据总样本数: {len(df_full)}")

# 孕周转换
def convert_week(week_str):
    if pd.isna(week_str):
        return np.nan
    week_str = str(week_str).strip()
    try:
        return float(week_str)
    except ValueError:
        pass
    if 'w' in week_str.lower():
        temp = week_str.lower().replace('w', '+')
        parts = temp.split('+')
        week = float(parts[0])
        if len(parts) > 1 and parts[1]:
            day_part = parts[1].replace('d', '').strip()
            if day_part:
                day = float(day_part)
                week += day / 7
        return week
    try:
        return float(week_str)
    except ValueError:
        return np.nan

df_full['孕周_数值'] = df_full['检测孕周'].apply(convert_week)

#筛选女胎
df_female = df_full[df_full['Y染色体浓度'].isna()].copy()
print(f"女胎样本数: {len(df_female)}")

#准备特征
features = [
    '孕周_数值', '孕妇BMI', '年龄',
    'X染色体的Z值', 'X染色体浓度',
    '13号染色体的Z值', '18号染色体的Z值', '21号染色体的Z值',
    '13号染色体的GC含量', '18号染色体的GC含量', '21号染色体的GC含量',
    'GC含量'
]

available_features = [f for f in features if f in df_female.columns]
print(f"可用特征数: {len(available_features)}")

#构建二分类标签
df_female['染色体的非整倍体'] = df_female['染色体的非整倍体'].fillna('正常')
df_female['标签'] = (df_female['染色体的非整倍体'] != '正常').astype(int)

# 查看分布
print("\n二分类标签分布:")
print(df_female['标签'].value_counts())
print(f"正常: {(df_female['标签']==0).sum()} 例")
print(f"异常: {(df_female['标签']==1).sum()} 例")

#清洗数据
df_clean = df_female[available_features + ['标签']].dropna()
print(f"清洗后样本数: {len(df_clean)}")

#建模
X = df_clean[available_features]
y = df_clean['标签']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# SMOTE处理不平衡
smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train_scaled, y_train)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_bal, y_train_bal)
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

print("\n" + "="*60)
print("女胎染色体异常检测结果")
print("="*60)
print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
print(f"精确率: {precision_score(y_test, y_pred):.4f}")
print(f"召回率: {recall_score(y_test, y_pred):.4f}")
print(f"F1分数: {f1_score(y_test, y_pred):.4f}")

print("\n分类报告:")
print(classification_report(y_test, y_pred, target_names=['正常', '异常']))

# 混淆矩阵
cm = confusion_matrix(y_test, y_pred)
print("\n混淆矩阵:")
print(f"           预测正常  预测异常")
print(f"实际正常      {cm[0,0]:>3}      {cm[0,1]:>3}")
print(f"实际异常      {cm[1,0]:>3}      {cm[1,1]:>3}")

#特征重要性
importances = model.feature_importances_
feature_importance = pd.DataFrame({
    '特征': available_features,
    '重要性': importances
}).sort_values('重要性', ascending=False)

print("\n特征重要性排名:")
print(feature_importance.to_string(index=False))
feature_importance.to_csv(r"D:\PythonProject1\数学建模\2025国赛C题\问题四\第四问_特征重要性.csv", index=False, encoding='utf-8-sig')