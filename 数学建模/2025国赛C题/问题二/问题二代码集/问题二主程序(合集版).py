import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import accuracy_score
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
np.random.seed(42)

#取数据
file_path = r"D:\PythonProject1\数学建模\2025国赛C题\原数据集\完整合并数据.csv"

df_full = pd.read_csv(file_path)

#根据Y浓度判断胎儿性别
# 男胎：Y染色体浓度非空；女胎：Y染色体浓度为空
df_full['胎儿性别'] = df_full['Y染色体浓度'].notna().astype(int)
male_count = df_full['胎儿性别'].sum()
female_count = len(df_full) - male_count
print(f"根据Y浓度判断性别：男胎 {male_count} 例，女胎 {female_count} 例")


#孕周转换函数
def convert_week(week_str):
    """将孕周转换为数值，支持多种格式"""
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


# 转换孕周
df_full['检测孕周_数值'] = df_full['检测孕周'].apply(convert_week)
df_full = df_full.dropna(subset=['检测孕周_数值'])
print(f"删除孕周无效样本后，剩余 {len(df_full)} 行")

# 女胎的Y浓度填充为0
df_full['Y染色体浓度'] = df_full['Y染色体浓度'].fillna(0)

#筛选男胎数据并计算中心化均值
df_male = df_full[df_full['胎儿性别'] == 1].copy()
print(f"\n男胎样本数: {len(df_male)}")
week_mean = df_male['检测孕周_数值'].mean()
print(f"男胎平均孕周: {week_mean:.4f} 周")
# 中心化
df_male['孕周_中心化'] = df_male['检测孕周_数值'] - week_mean
df_full['孕周_中心化'] = df_full['检测孕周_数值'] - week_mean

#拆分训练集和验证集
train_idx = np.random.choice(df_male.index, size=int(0.7 * len(df_male)), replace=False)
X_train = df_male.loc[train_idx, ['孕周_中心化', '孕妇BMI']]
y_train = df_male.loc[train_idx, 'Y染色体浓度']
X_val = df_male.drop(train_idx)[['孕周_中心化', '孕妇BMI']]
y_val = df_male.drop(train_idx)['Y染色体浓度']

print(f"训练集样本数: {len(X_train)}")
print(f"验证集样本数: {len(X_val)}")

#训练模型
X_train_with_const = sm.add_constant(X_train)
model = sm.OLS(y_train, X_train_with_const).fit(cov_type="HC3")

print("\n" + "=" * 70)
print("第一问最优模型参数")
print("=" * 70)
print(f"截距项: {model.params['const']:.4f}")
print(f"孕周_中心化系数: {model.params['孕周_中心化']:.4f}")
print(f"孕妇BMI系数: {model.params['孕妇BMI']:.4f}")
print(f"训练集调整R²: {model.rsquared_adj:.4f}")
print(f"残差标准差: {np.std(model.resid):.4f}")
print(f"训练集Y浓度均值: {np.mean(y_train):.4f}")
print("=" * 70)

#验证集评估
X_val_with_const = sm.add_constant(X_val)
y_val_pred = model.predict(X_val_with_const)
val_rmse = np.sqrt(np.mean((y_val - y_val_pred) ** 2))
print(f"验证集RMSE: {val_rmse:.4f}")

#全量数据残差校正
X_full_with_const = sm.add_constant(df_full[['孕周_中心化', '孕妇BMI']])
Y_pred = model.predict(X_full_with_const)
Y_adj = df_full['Y染色体浓度'].values - Y_pred.values + np.mean(y_train)

# 拆分男女胎
Y_male_raw = df_full[df_full['胎儿性别'] == 1]['Y染色体浓度'].values
Y_male_adj = Y_adj[df_full['胎儿性别'] == 1]
Y_female_raw = df_full[df_full['胎儿性别'] == 0]['Y染色体浓度'].values
Y_female_adj = Y_adj[df_full['胎儿性别'] == 0]
labels = df_full['胎儿性别'].values

print(f"\n男胎样本数（用于评估）: {len(Y_male_raw)}")
print(f"女胎样本数（用于评估）: {len(Y_female_raw)}")

#图1：校正前后分布对比
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.histplot(Y_male_raw, bins=20, kde=True, color='#1f77b4', edgecolor='white')
plt.title('校正前Y染色体浓度分布（男胎）', fontsize=14, pad=15)
plt.xlabel('Y染色体浓度', fontsize=12)
plt.ylabel('样本数', fontsize=12)
plt.grid(axis='y', alpha=0.3)

plt.subplot(1, 2, 2)
sns.histplot(Y_male_adj, bins=20, kde=True, color='#ff7f0e', edgecolor='white')
plt.title('校正后Y染色体浓度分布（男胎）', fontsize=14, pad=15)
plt.xlabel('Y染色体浓度', fontsize=12)
plt.ylabel('样本数', fontsize=12)
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('图1-校正前后Y浓度分布对比.png', dpi=300, bbox_inches='tight')
plt.show()

#手动ROC计算
def manual_roc_curve(y_true, y_score):
    thresholds = np.sort(np.unique(y_score))[::-1]
    fpr = []
    tpr = []

    for thresh in thresholds:
        y_pred = (y_score >= thresh).astype(int)
        TP = np.sum((y_true == 1) & (y_pred == 1))
        FP = np.sum((y_true == 0) & (y_pred == 1))
        TN = np.sum((y_true == 0) & (y_pred == 0))
        FN = np.sum((y_true == 1) & (y_pred == 0))

        fpr_val = FP / (FP + TN) if (FP + TN) > 0 else 0.0
        tpr_val = TP / (TP + FN) if (TP + FN) > 0 else 0.0

        fpr.append(fpr_val)
        tpr.append(tpr_val)

    fpr = np.array(fpr)
    tpr = np.array(tpr)

    # 按fpr排序并去重
    combined = np.column_stack((fpr, tpr))
    combined = combined[np.argsort(combined[:, 0])]
    _, unique_idx = np.unique(combined[:, 0], return_index=True)
    combined = combined[unique_idx]

    fpr = combined[:, 0]
    tpr = combined[:, 1]

    # 确保起点和终点
    if fpr[0] > 0:
        fpr = np.concatenate([[0], fpr])
        tpr = np.concatenate([[0], tpr])
    if fpr[-1] < 1:
        fpr = np.concatenate([fpr, [1]])
        tpr = np.concatenate([tpr, [1]])

    return fpr, tpr


# 校正前
fpr_raw, tpr_raw = manual_roc_curve(labels, df_full['Y染色体浓度'].values)
auc_raw = np.trapezoid(tpr_raw, fpr_raw)

# 校正后
fpr_adj, tpr_adj = manual_roc_curve(labels, Y_adj)
auc_adj = np.trapezoid(tpr_adj, fpr_adj)


# 计算最佳阈值
def find_best_threshold(y_true, y_score):
    thresholds = np.unique(y_score)
    best_thresh = 0.05
    best_youden = -1

    for thresh in thresholds:
        y_pred = (y_score >= thresh).astype(int)
        TP = np.sum((y_true == 1) & (y_pred == 1))
        FP = np.sum((y_true == 0) & (y_pred == 1))
        TN = np.sum((y_true == 0) & (y_pred == 0))
        FN = np.sum((y_true == 1) & (y_pred == 0))

        tpr = TP / (TP + FN) if (TP + FN) > 0 else 0
        fpr = FP / (FP + TN) if (FP + TN) > 0 else 0
        youden = tpr - fpr

        if youden > best_youden:
            best_youden = youden
            best_thresh = thresh

    return best_thresh


best_thresh_raw = find_best_threshold(labels, df_full['Y染色体浓度'].values)
best_thresh_adj = find_best_threshold(labels, Y_adj)


def calculate_metrics(y_true, y_pred_proba, threshold):
    y_pred = (y_pred_proba >= threshold).astype(int)
    acc = accuracy_score(y_true, y_pred)

    TP = np.sum((y_true == 1) & (y_pred == 1))
    FN = np.sum((y_true == 1) & (y_pred == 0))
    FP = np.sum((y_true == 0) & (y_pred == 1))
    TN = np.sum((y_true == 0) & (y_pred == 0))

    fnr = FN / (TP + FN) if (TP + FN) > 0 else 0
    fpr = FP / (FP + TN) if (FP + TN) > 0 else 0

    return acc, fnr, fpr


acc_raw, fnr_raw, fpr_raw_val = calculate_metrics(labels, df_full['Y染色体浓度'].values, best_thresh_raw)
acc_adj, fnr_adj, fpr_adj_val = calculate_metrics(labels, Y_adj, best_thresh_adj)

print("\n校正前后检测性能对比表")
print("-" * 70)
print(f"{'指标':<12} {'校正前':<10} {'校正后':<10} {'变化幅度':<10}")
print("-" * 70)
print(f"{'AUC':<12} {auc_raw:<10.4f} {auc_adj:<10.4f} {((auc_adj - auc_raw) / auc_raw * 100):<10.2f}%")
print(f"{'最佳阈值':<12} {best_thresh_raw:<10.4f} {best_thresh_adj:<10.4f} {'-':<10}")
print(f"{'准确率':<12} {acc_raw:<10.4f} {acc_adj:<10.4f} {((acc_adj - acc_raw) / acc_raw * 100):<10.2f}%")
print(
    f"{'假阴性率':<12} {fnr_raw:<10.4f} {fnr_adj:<10.4f} {((fnr_adj - fnr_raw) / fnr_raw * 100) if fnr_raw > 0 else 0:<10.2f}%")
print(
    f"{'假阳性率':<12} {fpr_raw_val:<10.4f} {fpr_adj_val:<10.4f} {((fpr_adj_val - fpr_raw_val) / fpr_raw_val * 100) if fpr_raw_val > 0 else 0:<10.2f}%")
print("-" * 70)

#图2：ROC曲线
plt.figure(figsize=(8, 8))
plt.plot(fpr_raw, tpr_raw, color='#1f77b4', lw=2, label=f'校正前 (AUC = {auc_raw:.4f})')
plt.plot(fpr_adj, tpr_adj, color='#ff7f0e', lw=2, label=f'校正后 (AUC = {auc_adj:.4f})')
plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--', label='随机猜测')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('假阳性率 (FPR)', fontsize=12)
plt.ylabel('真阳性率 (TPR)', fontsize=12)
plt.title('校正前后ROC曲线对比', fontsize=14, pad=15)
plt.legend(loc="lower right", fontsize=12)
plt.grid(alpha=0.3)
plt.savefig('图2-校正前后ROC曲线对比.png', dpi=300, bbox_inches='tight')
plt.show()

#BMI分组分析
def bmi_group(bmi):
    if bmi < 18.5:
        return '低体重'
    elif 18.5 <= bmi < 24:
        return '正常'
    elif 24 <= bmi < 28:
        return '超重'
    else:
        return '肥胖'


df_male['BMI分组'] = df_male['孕妇BMI'].apply(bmi_group)
groups = ['低体重', '正常', '超重', '肥胖']

fnr_raw_groups = []
fnr_adj_groups = []
group_counts = []

print("\n不同BMI组校正前后假阴性率对比")
print("-" * 70)
for group in groups:
    group_mask = df_male['BMI分组'] == group
    group_y_raw = df_male[group_mask]['Y染色体浓度'].values
    # 注意：Y_adj 是全量数据，需要对应男胎部分
    Y_adj_male = Y_adj[df_full['胎儿性别'] == 1]
    group_y_adj = Y_adj_male[group_mask.values]
    count = len(group_y_raw)

    if count == 0:
        fnr_raw_groups.append(0)
        fnr_adj_groups.append(0)
        group_counts.append(0)
        print(f"{group:<6} (n=0  ): 无样本")
        continue

    fnr_g_raw = np.mean(group_y_raw < best_thresh_raw)
    fnr_g_adj = np.mean(group_y_adj < best_thresh_adj)

    fnr_raw_groups.append(fnr_g_raw)
    fnr_adj_groups.append(fnr_g_adj)
    group_counts.append(count)

    change_pct = ((fnr_g_adj - fnr_g_raw) / fnr_g_raw * 100) if fnr_g_raw > 0 else 0
    print(f"{group:<6} (n={count:<3}): 校正前={fnr_g_raw:.4f} | 校正后={fnr_g_adj:.4f} | 变化={change_pct:+.2f}%")
print("-" * 70)

# 图3：分组假阴性率对比
plt.figure(figsize=(10, 6))
x = np.arange(len(groups))
width = 0.35

plt.bar(x - width / 2, fnr_raw_groups, width, label='校正前', color='#1f77b4', alpha=0.8)
plt.bar(x + width / 2, fnr_adj_groups, width, label='校正后', color='#ff7f0e', alpha=0.8)

plt.xlabel('BMI分组', fontsize=12)
plt.ylabel('假阴性率', fontsize=12)
plt.title('不同BMI组校正前后假阴性率对比', fontsize=14, pad=15)
plt.xticks(x, groups, fontsize=11)
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.savefig('图3-不同BMI组假阴性率对比.png', dpi=300, bbox_inches='tight')
plt.show()

#个性化阈值表
print("\n【个性化阈值示例表】")
print("-" * 70)
print(f"{'孕周(周)':<10} {'BMI':<8} {'个性化阈值':<12} {'适用人群'}")
print("-" * 70)

resid_std = np.std(model.resid)
for week, bmi, desc in [
    (12, 35, "早孕+肥胖"),
    (13, 32, "中孕+超重"),
    (14, 28, "中孕+正常"),
    (15, 24, "晚孕+低体重"),
    (16, 20, "晚孕+偏瘦")
]:
    week_c = week - week_mean
    baseline = model.params['const'] + model.params['孕周_中心化'] * week_c + model.params['孕妇BMI'] * bmi
    threshold = baseline - 1.96 * resid_std
    print(f"{week:<10} {bmi:<8} {threshold:<12.4f} {desc}")
print("-" * 70)