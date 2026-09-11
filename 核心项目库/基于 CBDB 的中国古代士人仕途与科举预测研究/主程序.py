import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

df = pd.read_csv('cbdb_final_data.csv')

# 1. 提取方氏数据
fang_df = df[df['c_surname_chn'] == '方'].copy()
print(f"方氏总人数：{len(fang_df)}")
print(f"有传记的人数：{len(fang_df[fang_df['c_self_bio']==1])}")
print(f"有传记比例：{len(fang_df[fang_df['c_self_bio']==1])/len(fang_df):.2%}")

# 2. 看时间分布
fang_df['c_index_year'] = pd.to_numeric(fang_df['c_index_year'], errors='coerce')
fang_year_dist = fang_df['c_index_year'].dropna()

plt.figure(figsize=(12,5))
plt.hist(fang_year_dist, bins=30)
plt.title('方氏人物时间分布')
plt.xlabel('年份')
plt.ylabel('人数')
plt.show()

# 3. 看地域分布
fang_addr = fang_df['c_index_addr_id'].value_counts().head(20)
print("\n方氏主要分布地址：")
print(fang_addr)


def build_fang_importance_label(row):
    """
    构建方氏人物重要性评分
    分数范围 0-5
    """
    score = 0

    # 基础：有传记
    if row['c_self_bio'] == 1:
        score += 1

    # 官职 (c_dy 可能代表官职等级)
    if pd.notna(row['c_dy']) and row['c_dy'] > 0:
        # 假设 c_dy 越大官职越高
        if row['c_dy'] > 10:
            score += 2
        elif row['c_dy'] > 5:
            score += 1

    # 有生卒年记录（说明史料详细）
    if pd.notna(row['c_birthyear']) and row['c_birthyear'] > 0:
        score += 1

    # 有活动年份记录（说明有事迹）
    if (pd.notna(row['c_fl_earliest_year']) and row['c_fl_earliest_year'] > 0) or \
            (pd.notna(row['c_fl_latest_year']) and row['c_fl_latest_year'] > 0):
        score += 1

    # 去世年龄较大（可能官职更高、更成功）
    if pd.notna(row['c_death_age']) and row['c_death_age'] > 60:
        score += 1

    # 转化为二分类：>=3 为重要，<3 为不重要
    return 1 if score >= 3 else 0


fang_df['importance'] = fang_df.apply(build_fang_importance_label, axis=1)
print(f"重要人物比例：{fang_df['importance'].mean():.2%}")

# 划分时期 - 先确保c_index_year是数值类型
def period_label(year):
    if pd.isna(year):
        return 'other'
    if year < 900:
        return 'pre_tang'
    elif 900 <= year < 960:
        return 'five_dynasties'
    elif 960 <= year < 1127:
        return 'northern_song'
    elif 1127 <= year < 1279:
        return 'southern_song'
    else:
        return 'other'

fang_df['period'] = fang_df['c_index_year'].apply(period_label)

# 相对时间：距离家族第一次出现的时间
first_fang_year = fang_df['c_index_year'].min()
fang_df['years_since_first'] = fang_df['c_index_year'] - first_fang_year

# 计算每个地址的整体成功率（用整个数据集）
addr_success = df.groupby('c_index_addr_id')['c_self_bio'].mean().to_dict()
fang_df['addr_success_rate'] = fang_df['c_index_addr_id'].map(addr_success)

# 方氏在该地址的聚集度
fang_addr_count = fang_df.groupby('c_index_addr_id').size().to_dict()
fang_df['fang_cluster_size'] = fang_df['c_index_addr_id'].map(fang_addr_count)

# 是否为方氏核心区域（方氏人数最多的前5个地址）
top_fang_addrs = fang_df['c_index_addr_id'].value_counts().nlargest(5).index
fang_df['is_core_area'] = fang_df['c_index_addr_id'].isin(top_fang_addrs).astype(int)

# 同一地址、同一时期是否有其他方氏成功者
def count_fang_success_in_area(row, data):
    mask = (data['c_index_addr_id'] == row['c_index_addr_id']) & \
           (data['period'] == row['period']) & \
           (data['importance'] == 1)
    return mask.sum()

fang_df['fang_success_in_area'] = fang_df.apply(
    lambda row: count_fang_success_in_area(row, fang_df), axis=1
)

# 是否与成功者同地址（排除自己）
fang_df['has_fang_success_neighbor'] = fang_df['fang_success_in_area'] > 1

# 按时间排序，看是否来自"成功家族分支"
fang_sorted = fang_df.sort_values('c_index_year')
fang_sorted['prev_gen_success'] = 0

# 简单的前后50年窗口
for idx, row in fang_sorted.iterrows():
    if pd.notna(row['c_index_year']):
        window_start = row['c_index_year'] - 50
        window_end = row['c_index_year'] - 10
        prev_success = fang_sorted[
            (fang_sorted['c_index_year'] >= window_start) &
            (fang_sorted['c_index_year'] <= window_end) &
            (fang_sorted['importance'] == 1)
        ]
        fang_sorted.loc[idx, 'prev_gen_success'] = len(prev_success)

fang_df['prev_gen_success'] = fang_sorted['prev_gen_success']

# 为整个数据集创建period列，用于计算社会基准成功率
df['c_index_year'] = pd.to_numeric(df['c_index_year'], errors='coerce')
df['period'] = df['c_index_year'].apply(period_label)

# 该时期整个社会的成功基准
period_success_rate = df.groupby('period')['c_self_bio'].mean().to_dict()
fang_df['period_success_rate'] = fang_df['period'].map(period_success_rate)

# 方氏在该时期的相对表现
fang_period_rate = fang_df.groupby('period')['importance'].mean().to_dict()
fang_df['fang_period_rate'] = fang_df['period'].map(fang_period_rate)
fang_df['fang_vs_society'] = fang_df['fang_period_rate'] - fang_df['period_success_rate']

# 选择特征
feature_cols = [
    'c_index_year', 'years_since_first',
    'addr_success_rate', 'fang_cluster_size', 'is_core_area',
    'fang_success_in_area', 'prev_gen_success',
    'period_success_rate', 'fang_vs_society'
]

# 处理分类变量
le = LabelEncoder()
fang_df['period_encoded'] = le.fit_transform(fang_df['period'].fillna('other'))

# 添加时期编码
feature_cols_with_encoded = feature_cols + ['period_encoded']

# 处理缺失值
X = fang_df[feature_cols_with_encoded].fillna(0)
y = fang_df['importance']

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 随机森林
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    class_weight='balanced',
    random_state=42
)
rf_model.fit(X_train, y_train)

# XGBoost
xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train) if sum(y_train) > 0 else 1,  # 处理不平衡
    random_state=42,
    eval_metric='logloss'
)
xgb_model.fit(X_train, y_train)

# 评估
for name, model in [('Random Forest', rf_model), ('XGBoost', xgb_model)]:
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    print(f"\n=== {name} ===")
    print(classification_report(y_test, y_pred))
    print(f"AUC: {roc_auc_score(y_test, y_prob):.3f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

# 随机森林特征重要性
feature_importance = pd.DataFrame({
    'feature': feature_cols_with_encoded,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n=== 特征重要性 ===")
print(feature_importance)

# 可视化
plt.figure(figsize=(10,6))
plt.barh(feature_importance['feature'][:10], feature_importance['importance'][:10])
plt.title('Top 10 重要特征（方氏家族）')
plt.xlabel('重要性')
plt.tight_layout()
plt.show()