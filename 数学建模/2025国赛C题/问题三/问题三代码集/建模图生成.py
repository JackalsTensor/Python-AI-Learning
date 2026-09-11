import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import norm
import warnings

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
np.random.seed(42)

#读取并预处理数据
file_path = r"D:\PythonProject1\数学建模\2025国赛C题\原数据集\完整合并数据.csv"
df_full = pd.read_csv(file_path)

#只保留男胎样本
df_male = df_full[df_full['Y染色体浓度'].notna()].copy()
print(f"筛选男胎样本，共 {len(df_male)} 行")


# 孕周转换函数
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


# 数据清洗
df_male['检测孕周_数值'] = df_male['检测孕周'].apply(convert_week)
df_male = df_male.dropna(subset=['检测孕周_数值', '孕妇BMI', '年龄'])

# 剔除异常值
df_male = df_male[(df_male['检测孕周_数值'] >= 10) & (df_male['检测孕周_数值'] <= 25)]
df_male = df_male[(df_male['孕妇BMI'] >= 15) & (df_male['孕妇BMI'] <= 50)]
df_male = df_male[(df_male['Y染色体浓度'] >= 0) & (df_male['Y染色体浓度'] <= 1)]

print(f"清洗后有效男胎样本数: {len(df_male)} 行")

# 特征工程
week_mean = df_male['检测孕周_数值'].mean()
df_male['孕周_中心化'] = df_male['检测孕周_数值'] - week_mean
df_male['孕周_平方'] = df_male['孕周_中心化'] ** 2
df_male['孕周_BMI交互'] = df_male['孕周_中心化'] * df_male['孕妇BMI']

# 年龄中心化
age_mean = df_male['年龄'].mean()
df_male['年龄_中心化'] = df_male['年龄'] - age_mean

#构建增强型Y浓度预测模型
X = df_male[['孕周_中心化', '孕周_平方', '孕妇BMI', '年龄_中心化', '孕周_BMI交互']]
X = sm.add_constant(X)
y = df_male['Y染色体浓度']

model = sm.OLS(y, X).fit(cov_type="HC3")
print("\n" + "=" * 70)
print("问题三增强型回归模型结果")
print("=" * 70)
print(model.summary())
print("=" * 70)

sigma_model = np.std(model.resid)
print(f"\n模型残差标准差: {sigma_model:.4f}")
print(f"训练集调整R²: {model.rsquared_adj:.4f}")

# 提取模型参数
model_params = {
    'const': model.params['const'],
    '孕周_中心化': model.params['孕周_中心化'],
    '孕周_平方': model.params['孕周_平方'],
    '孕妇BMI': model.params['孕妇BMI'],
    '年龄_中心化': model.params['年龄_中心化'],
    '孕周_BMI交互': model.params['孕周_BMI交互']
}

# ===================== 3. 定义核心函数 =====================
def sequencing_failure_rate(t):
    if t < 10:
        return 1.0
    return 0.3 * np.exp(-0.2 * (t - 10))


def time_risk(t):
    if t <= 12:
        return 1.0
    else:
        return np.exp(0.15 * (t - 12))


def calculate_metrics_for_individual(row, t, sigma_total, week_mean, model_params):
    week_c = t - week_mean
    week_sq = week_c ** 2
    bmi = row['孕妇BMI']
    age_c = row['年龄_中心化']
    interaction = week_c * bmi

    y_pred = (model_params['const'] +
              model_params['孕周_中心化'] * week_c +
              model_params['孕周_平方'] * week_sq +
              model_params['孕妇BMI'] * bmi +
              model_params['年龄_中心化'] * age_c +
              model_params['孕周_BMI交互'] * interaction)

    threshold = 0.04
    p_pass = 1 - norm.cdf((threshold - y_pred) / sigma_total)
    fnr = norm.cdf((threshold - y_pred) / sigma_total) if y_pred >= threshold else 1.0
    p_fail = sequencing_failure_rate(t)

    p_success = (1 - p_fail) * (1 - fnr)
    risk_success = time_risk(t)
    risk_fail = time_risk(t + 2)
    total_risk = p_success * risk_success + (1 - p_success) * risk_fail

    return y_pred, p_pass, fnr, p_fail, total_risk


def calculate_group_metrics(group_df, t, sigma_total, week_mean, model_params):
    metrics = group_df.apply(lambda row: calculate_metrics_for_individual(row, t, sigma_total, week_mean, model_params),
                             axis=1)
    p_passes = [m[1] for m in metrics]
    total_risks = [m[4] for m in metrics]
    return {
        '达标比例': np.mean(p_passes),
        '平均总风险': np.mean(total_risks)
    }


#BMI分组
def bmi_group(bmi):
    if bmi < 18.5:
        return '低体重'
    elif 18.5 <= bmi < 24:
        return '正常体重'
    elif 24 <= bmi < 28:
        return '超重'
    elif 28 <= bmi < 32:
        return '轻度肥胖'
    elif 32 <= bmi < 36:
        return '中度肥胖'
    elif 36 <= bmi < 40:
        return '重度肥胖'
    else:
        return '极重度肥胖'


df_male['BMI分组'] = df_male['孕妇BMI'].apply(bmi_group)
groups = ['正常体重', '超重', '轻度肥胖', '中度肥胖', '重度肥胖', '极重度肥胖']

print("\nBMI分组样本统计")
for group in groups:
    count = len(df_male[df_male['BMI分组'] == group])
    print(f"{group:<10} {count:>4} 例")

#求解最佳时点
sigma_measure = 0.01
sigma_total_base = np.sqrt(sigma_model ** 2 + sigma_measure ** 2)
target_pass_rate = 0.95
week_range = np.arange(10.0, 25.1, 0.1)

best_results = []

for group in groups:
    group_df = df_male[df_male['BMI分组'] == group].copy()
    if len(group_df) == 0:
        best_results.append([group, np.nan])
        continue

    group_metrics = []
    for t in week_range:
        metrics = calculate_group_metrics(group_df, t, sigma_total_base, week_mean, model_params)
        metrics['孕周'] = t
        group_metrics.append(metrics)

    group_metrics_df = pd.DataFrame(group_metrics)
    valid_df = group_metrics_df[group_metrics_df['达标比例'] >= target_pass_rate]

    if len(valid_df) == 0:
        best_idx = group_metrics_df['达标比例'].idxmax()
        best_t = group_metrics_df.iloc[best_idx]['孕周']
    else:
        best_idx = valid_df['平均总风险'].idxmin()
        best_t = valid_df.loc[best_idx]['孕周']

    best_results.append([group, best_t])

#图1：Y浓度随孕周变化曲线
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

plt.figure(figsize=(12, 8))
for i, group in enumerate(groups):
    group_df = df_male[df_male['BMI分组'] == group].copy()
    if len(group_df) == 0:
        continue

    y_means = []
    y_lower = []
    y_upper = []

    for t in week_range:
        week_c = t - week_mean
        week_sq = week_c ** 2
        bmi_mean = group_df['孕妇BMI'].mean()
        age_c_mean = group_df['年龄_中心化'].mean()
        interaction = week_c * bmi_mean

        y_pred = (model_params['const'] +
                  model_params['孕周_中心化'] * week_c +
                  model_params['孕周_平方'] * week_sq +
                  model_params['孕妇BMI'] * bmi_mean +
                  model_params['年龄_中心化'] * age_c_mean +
                  model_params['孕周_BMI交互'] * interaction)

        y_means.append(y_pred)
        y_lower.append(y_pred - 1.96 * sigma_total_base)
        y_upper.append(y_pred + 1.96 * sigma_total_base)

    plt.plot(week_range, y_means, color=colors[i], lw=2, label=group)
    plt.fill_between(week_range, y_lower, y_upper, color=colors[i], alpha=0.2)

plt.axhline(y=0.04, color='red', linestyle='--', lw=2, label='4%达标线')
plt.xlabel('检测孕周(周)', fontsize=12)
plt.ylabel('Y染色体浓度', fontsize=12)
plt.title('不同BMI组Y染色体浓度随孕周变化曲线', fontsize=14)
plt.legend(fontsize=10)
plt.grid(alpha=0.3)
plt.savefig('图3-1-不同BMI组Y浓度变化曲线.png', dpi=300, bbox_inches='tight')
plt.show()

#图2：总风险随孕周变化曲线
plt.figure(figsize=(12, 8))
for i, group in enumerate(groups):
    group_df = df_male[df_male['BMI分组'] == group].copy()
    if len(group_df) == 0:
        continue

    risks = []
    for t in week_range:
        metrics = calculate_group_metrics(group_df, t, sigma_total_base, week_mean, model_params)
        risks.append(metrics['平均总风险'])

    plt.plot(week_range, risks, color=colors[i], lw=2, label=group)

    # 标注最佳时点
    best_t = best_results[i][1]
    if not np.isnan(best_t):
        idx = np.argmin(np.abs(week_range - best_t))
        plt.scatter(best_t, risks[idx], color=colors[i], s=100, zorder=5)
        plt.text(best_t + 0.3, risks[idx], f'{best_t:.1f}周', fontsize=9)

plt.xlabel('检测孕周(周)', fontsize=12)
plt.ylabel('平均总风险', fontsize=12)
plt.title('不同BMI组总风险随孕周变化曲线', fontsize=14)
plt.legend(fontsize=10)
plt.grid(alpha=0.3)
plt.savefig('图3-2-不同BMI组风险变化曲线.png', dpi=300, bbox_inches='tight')
plt.show()

#8. 读取敏感性分析结果并绘图
sigma_levels = [0.02, 0.03, 0.04, 0.05, 0.06]
sensitivity_results = []

for sigma in sigma_levels:
    row = [sigma]
    for group in groups:
        group_df = df_male[df_male['BMI分组'] == group].copy()
        if len(group_df) == 0:
            row.append(np.nan)
            continue

        group_metrics = []
        for t in week_range:
            metrics = calculate_group_metrics(group_df, t, sigma, week_mean, model_params)
            metrics['孕周'] = t
            group_metrics.append(metrics)

        group_metrics_df = pd.DataFrame(group_metrics)
        valid_df = group_metrics_df[group_metrics_df['达标比例'] >= target_pass_rate]

        if len(valid_df) == 0:
            best_idx = group_metrics_df['达标比例'].idxmax()
            best_t = group_metrics_df.iloc[best_idx]['孕周']
        else:
            best_idx = valid_df['平均总风险'].idxmin()
            best_t = valid_df.loc[best_idx]['孕周']
        row.append(best_t)

    sensitivity_results.append(row)

sensitivity_columns = ['总误差标准差'] + groups
sensitivity_df = pd.DataFrame(sensitivity_results, columns=sensitivity_columns)

#图3：检测误差敏感性分析
plt.figure(figsize=(10, 6))
for i, group in enumerate(groups):
    if group in sensitivity_df.columns:
        plt.plot(sensitivity_df['总误差标准差'], sensitivity_df[group],
                 color=colors[i], lw=2, marker='o', label=group)

plt.xlabel('总检测误差标准差', fontsize=12)
plt.ylabel('最佳检测时点(周)', fontsize=12)
plt.title('检测误差对最佳检测时点的影响', fontsize=14)
plt.legend(fontsize=10)
plt.grid(alpha=0.3)
plt.savefig('图3-3-检测误差敏感性分析.png', dpi=300, bbox_inches='tight')
plt.show()