import pandas as pd
import numpy as np
import os

# 1. 读取男胎原数据集
file_path = r"D:\PythonProject1\数学建模\2025国赛C题\原数据集\男胎检测数据.csv"
df_male = pd.read_csv(file_path)
print(f"原始男胎数据总行数: {df_male.shape[0]}，总列数: {df_male.shape[1]}")

# 2. 去掉列名前后空格
df_male.columns = df_male.columns.str.strip()

# 3. 孕周连续化(处理成连续数值便于后续数据分析)
preg_week_col = '检测孕周'
def week_to_float(week_str):
    try:
        if '+' in str(week_str):
            w, d = week_str.split('+')
            return float(w) + float(d)/7
        else:
            return float(week_str)
    except:
        return np.nan

df_male['孕周_连续'] = df_male[preg_week_col].apply(week_to_float)

# 4. 统一缺失值
df_male.replace(['', 'NA', 'null', None], np.nan, inplace=True)

# 5. 删除绝对异常值(确保后续数据分析合理性)
bmi_col = '孕妇BMI'
df_male = df_male[(df_male[bmi_col] >= 15) & (df_male[bmi_col] <= 50)]

gc_col = 'GC含量'
df_male = df_male[(df_male[gc_col] >= 0.4) & (df_male[gc_col] <= 0.6)]

age_col = '年龄'
df_male = df_male[(df_male[age_col] >= 15) & (df_male[age_col] <= 50)]

y_col = 'Y染色体浓度'
df_male = df_male[(df_male[y_col] >= 0) & (df_male[y_col] <= 15)]

# 6. 删除完全重复样本
df_male.drop_duplicates(inplace=True)

# 7. 处理重复检测
df_male = df_male.drop_duplicates(subset=['孕妇代码', '检测日期'])

# 8. 数据类型统一
numeric_cols = [
    '年龄','身高','体重','孕周_连续','孕妇BMI','原始读段数',
    '在参考基因组上比对的比例','重复读段的比例','唯一比对的读段数  ','GC含量',
    '13号染色体的Z值','18号染色体的Z值','21号染色体的Z值',
    'X染色体的Z值','Y染色体的Z值','Y染色体浓度','X染色体浓度',
    '13号染色体的GC含量','18号染色体的GC含量','21号染色体的GC含量',
    '被过滤掉读段数的比例','怀孕次数','生产次数'
]

for col in numeric_cols:
    if col in df_male.columns:
        df_male[col] = pd.to_numeric(df_male[col], errors='coerce')

# 9. 保存清洗后的男胎全局数据
output_dir = r"D:\PythonProject1\数学建模\2025国赛C题\清洗后数据集"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_path = os.path.join(output_dir, "全局清洗后男胎_clean.csv")
df_male.to_csv(output_path, index=False)
print("男胎全局清洗完成，保存为:", output_path)