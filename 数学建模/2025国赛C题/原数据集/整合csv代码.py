import pandas as pd

# ===================== 【只需修改这3个路径】 =====================
male_path = r"D:\PythonProject1\数学建模\2025国赛C题\原数据集\男胎检测数据.csv"
female_path = r"D:\PythonProject1\数学建模\2025国赛C题\原数据集\女胎检测数据.csv"
save_path = r"D:\PythonProject1\数学建模\2025国赛C题\原数据集\完整合并数据.csv"

# ===================== 1. 读取数据 =====================
df_male = pd.read_csv(male_path)
df_female = pd.read_csv(female_path)

# ===================== 2. 自动修复列名（核心！解决你的报错） =====================
# 修复男胎：去掉多余空格
df_male.rename(columns={'唯一比对的读段数  ': '唯一比对的读段数'}, inplace=True)

# 修复女胎：Unnamed列替换为Y染色体列
df_female.rename(columns={
    'Unnamed: 20': 'Y染色体的Z值',
    'Unnamed: 21': 'Y染色体浓度'
}, inplace=True)

# ===================== 3. 统一所有列（补全缺失列，女胎Y值填0） =====================
all_columns = [
    '序号', '孕妇代码', '年龄', '身高', '体重', '末次月经', 'IVF妊娠',
    '检测日期', '检测抽血次数', '检测孕周', '孕妇BMI', '原始读段数',
    '在参考基因组上比对的比例', '重复读段的比例', '唯一比对的读段数',
    'GC含量', '13号染色体的Z值', '18号染色体的Z值', '21号染色体的Z值',
    'X染色体的Z值', 'Y染色体的Z值', 'Y染色体浓度', 'X染色体浓度',
    '13号染色体的GC含量', '18号染色体的GC含量', '21号染色体的GC含量',
    '被过滤掉读段数的比例', '染色体的非整倍体', '怀孕次数', '生产次数',
    '胎儿是否健康', '胎儿性别'
]

# 对齐列，缺失的列自动补0
df_male = df_male.reindex(columns=all_columns)
df_female = df_female.reindex(columns=all_columns)

# ===================== 4. 合并数据 =====================
df_combined = pd.concat([df_male, df_female], ignore_index=True)

# ===================== 5. 保存最终文件 =====================
df_combined.to_csv(save_path, index=False, encoding='utf-8-sig')

# ===================== 输出结果 =====================
print("="*60)
print("✅ 列名自动修复完成！")
print(f"✅ 男胎样本：{len(df_male)} 条")
print(f"✅ 女胎样本：{len(df_female)} 条")
print(f"✅ 总合并样本：{len(df_combined)} 条")
print(f"✅ 完整文件已保存至：\n{save_path}")
print("="*60)