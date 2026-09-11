import pandas as pd
import numpy as np

# ---------------------- 1. 读取数据（解决分隔符/列名问题） ----------------------
# 数据集说明：这是心脏病诊断数据，无表头，先手动定义列名（适配UCI原始数据集格式）
col_names = [
    "age",        # 年龄
    "sex",        # 性别：1=男，0=女
    "cp",         # 胸痛类型：1=典型心绞痛，2=非典型心绞痛，3=非心绞痛，4=无症状
    "trestbps",   # 静息血压（mm Hg）
    "chol",       # 血清胆固醇（mg/dl）
    "fbs",        # 空腹血糖>120mg/dl：1=是，0=否
    "restecg",    # 静息心电图结果：0=正常，1=有ST-T波异常，2=左心室肥大
    "thalach",    # 最大心率
    "exang",      # 运动诱发心绞痛：1=是，0=否
    "oldpeak",    # ST段压低（由运动相对静息引起）
    "slope",      # ST段峰值斜率：1=上坡，2=平坦，3=下坡
    "ca",         # 荧光检查着色的主要血管数（0-3）
    "thal",       # 地中海贫血：3=正常，6=固定缺陷，7=可逆缺陷
    "target"      # 诊断结果：0=无心脏病，1-4=有心脏病（不同程度）
]

# 读取数据（处理分隔符+缺失值+列名）
# 注意：数据集里的缺失值用"?"表示，读取时要指定
df = pd.read_csv(
    "processed.cleveland.data",  # 你的数据文件名
    sep=",",                     # 分隔符（逗号）
    names=col_names,             # 手动加列名
    na_values="?"                # 把"?"识别为缺失值
)

# ---------------------- 2. 初步清洗（处理缺失值/数据类型） ----------------------
print("===== 数据基本信息 =====")
print(f"数据形状（行×列）：{df.shape}")
print("\n缺失值统计：")
print(df.isnull().sum())  # 查看每列缺失值数量

# 处理缺失值（简单策略：删除含缺失值的行，适合入门）
df = df.dropna(axis=0, how="any")
print(f"\n删除缺失值后数据形状：{df.shape}")

# 修正数据类型（部分列读取后是字符串，转为数值型）
df = df.astype({
    "ca": float,
    "thal": float,
    "target": int  # 标签转为整数
})

# ---------------------- 3. 数据探索（快速了解数据分布） ----------------------
print("\n===== 数据统计描述 =====")
print(df.describe())  # 数值列的均值/标准差/最值等

# 查看目标变量分布（有多少人有心脏病）
print("\n===== 心脏病诊断结果分布 =====")
target_count = df["target"].value_counts()
print(target_count)
# 简化标签：0=无心脏病，≥1=有心脏病
df["target_simple"] = df["target"].apply(lambda x: 1 if x >= 1 else 0)
print("\n简化后标签分布（0=无病，1=有病）：")
print(df["target_simple"].value_counts())

# ---------------------- 4. 简单可视化（看年龄和心率的关系） ----------------------
# 可选：如果想画图，先确保安装了matplotlib（没装的话先跑：pip install matplotlib）
try:
    import matplotlib.pyplot as plt
    # 按是否患病分组，画年龄和最大心率的散点图
    plt.figure(figsize=(10, 6))
    # 无病组（蓝色）
    plt.scatter(df[df["target_simple"]==0]["age"],
                df[df["target_simple"]==0]["thalach"],
                c="blue", label="无心脏病", alpha=0.7)
    # 患病组（红色）
    plt.scatter(df[df["target_simple"]==1]["age"],
                df[df["target_simple"]==1]["thalach"],
                c="red", label="有心脏病", alpha=0.7)
    plt.xlabel("年龄")
    plt.ylabel("最大心率")
    plt.title("年龄 vs 最大心率（按心脏病诊断结果分组）")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()
except ImportError:
    print("\n提示：未安装matplotlib，跳过画图步骤（可运行 pip install matplotlib 安装）")

# ---------------------- 5. 保存清洗后的数据（可选） ----------------------
# 把清洗好的数据存为新的CSV，方便后续建模
df.to_csv("heart_disease_cleaned.csv", index=False)
print("\n✅ 清洗后的数据已保存为：heart_disease_cleaned.csv")