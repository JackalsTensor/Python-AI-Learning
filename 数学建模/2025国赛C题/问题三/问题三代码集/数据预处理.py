import pandas as pd
import numpy as np
import statsmodels.api as sm
import os
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
print("-" * 50)
for group in groups:
    count = len(df_male[df_male['BMI分组'] == group])
    print(f"{group:<10} {count:>4} 例")