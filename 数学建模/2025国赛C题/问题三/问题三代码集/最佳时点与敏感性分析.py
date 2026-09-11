import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import norm
import warnings

warnings.filterwarnings('ignore')
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
print("问题三增强型回归模型结果")
print(model.summary())

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

#定义核心函数
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

#求解各组最佳检测时点
sigma_measure = 0.01
sigma_total_base = np.sqrt(sigma_model ** 2 + sigma_measure ** 2)
target_pass_rate = 0.95
week_range = np.arange(10.0, 25.1, 0.1)

best_results = []

print("\n各组最佳检测时点求解结果")
print(f"{'BMI分组':<10} {'最佳时点(周)':<12} {'达标比例(%)':<12} {'平均总风险':<12}")

for group in groups:
    group_df = df_male[df_male['BMI分组'] == group].copy()
    if len(group_df) == 0:
        best_results.append([group, np.nan, np.nan, np.nan])
        print(f"{group:<10} {'无样本':<12} {'-':<12} {'-':<12}")
        continue

    group_metrics = []
    for t in week_range:
        metrics = calculate_group_metrics(group_df, t, sigma_total_base, week_mean, model_params)
        metrics['孕周'] = t
        group_metrics.append(metrics)

    group_metrics_df = pd.DataFrame(group_metrics)

    # 筛选满足达标比例的孕周
    valid_df = group_metrics_df[group_metrics_df['达标比例'] >= target_pass_rate]

    if len(valid_df) == 0:
        # 没有满足条件的时点，取达标比例最高的时点
        best_idx = group_metrics_df['达标比例'].idxmax()
        best_metrics = group_metrics_df.iloc[best_idx]
        best_t = best_metrics['孕周']
        pass_rate = best_metrics['达标比例'] * 100
        total_risk = best_metrics['平均总风险']
        print(f"{group:<10} {best_t:<12.1f} {pass_rate:<12.1f} {total_risk:<12.2f} (⚠️未达95%)")
    else:
        # 在满足条件的时点中找风险最小的
        best_idx = valid_df['平均总风险'].idxmin()
        best_metrics = valid_df.loc[best_idx]
        best_t = best_metrics['孕周']
        pass_rate = best_metrics['达标比例'] * 100
        total_risk = best_metrics['平均总风险']
        print(f"{group:<10} {best_t:<12.1f} {pass_rate:<12.1f} {total_risk:<12.2f}")

    best_results.append([group, best_t, pass_rate, total_risk])

best_results_df = pd.DataFrame(best_results, columns=['BMI分组', '最佳时点(周)', '达标比例(%)', '平均总风险'])
best_results_df.to_csv('问题三-最佳检测时点结果.csv', index=False, encoding='utf-8-sig')

#检测误差敏感性分析
print("\n检测误差敏感性分析")
print("=" * 70)

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
print("\n不同误差水平下的最佳检测时点(周)")
print(sensitivity_df.to_string(index=False))
sensitivity_df.to_csv('问题三-检测误差敏感性分析.csv', index=False, encoding='utf-8-sig')