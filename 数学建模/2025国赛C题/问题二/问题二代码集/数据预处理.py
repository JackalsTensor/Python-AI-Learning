import pandas as pd
import numpy as np
import warnings
from matplotlib import pyplot as plt

warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
np.random.seed(42)

#读取数据
file_path = r"D:\PythonProject1\数学建模\2025国赛C题\原数据集\完整合并数据.csv"
df_full = pd.read_csv(file_path)

#根据Y浓度判断胎儿性别
df_full['胎儿性别'] = df_full['Y染色体浓度'].notna().astype(int)

male_count = df_full['胎儿性别'].sum()
female_count = len(df_full) - male_count
print(f"根据Y浓度判断性别：男胎 {male_count} 例，女胎 {female_count} 例")

#孕周转换函数
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

df_full['检测孕周_数值'] = df_full['检测孕周'].apply(convert_week)
df_full = df_full.dropna(subset=['检测孕周_数值'])
print(f"删除孕周无效样本后，剩余 {len(df_full)} 行")

df_full['Y染色体浓度'] = df_full['Y染色体浓度'].fillna(0)

#筛选男胎数据并计算中心化均值
df_male = df_full[df_full['胎儿性别'] == 1].copy()
print(f"\n男胎样本数: {len(df_male)}")

week_mean = df_male['检测孕周_数值'].mean()
print(f"男胎平均孕周: {week_mean:.4f} 周")

df_male['孕周_中心化'] = df_male['检测孕周_数值'] - week_mean
df_full['孕周_中心化'] = df_full['检测孕周_数值'] - week_mean

#拆分训练集
train_idx = np.random.choice(df_male.index, size=int(0.7 * len(df_male)), replace=False)
X_train = df_male.loc[train_idx, ['孕周_中心化', '孕妇BMI']]
y_train = df_male.loc[train_idx, 'Y染色体浓度']
X_val = df_male.drop(train_idx)[['孕周_中心化', '孕妇BMI']]
y_val = df_male.drop(train_idx)['Y染色体浓度']

print(f"训练集样本数: {len(X_train)}")
print(f"验证集样本数: {len(X_val)}")