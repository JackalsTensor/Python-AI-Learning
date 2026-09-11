import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

MALE_CLEAN_PATH = r"/数学建模/2025国赛C题/清洗后数据集/全局清洗后男胎_clean.csv"

plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams['figure.dpi'] = 120

# 1. 读取数据 + 基础清洗
df = pd.read_csv(MALE_CLEAN_PATH)

# 第一步：清理列名里的空格
df.columns = df.columns.str.strip()

# 第二步：手动清洗数值列，去掉空格/非数字字符，避免数据被清空
def clean_numeric(x):
    if pd.isna(x):
        return np.nan
    # 转字符串，去掉所有空格、非数字字符
    s = str(x).strip()
    # 只保留数字和小数点
    s = ''.join([c for c in s if c in '0123456789.'])
    try:
        return float(s)
    except:
        return np.nan

# 清洗核心列
df["检测孕周"] = df["检测孕周"].apply(clean_numeric)
df["孕妇BMI"] = df["孕妇BMI"].apply(clean_numeric)
df["Y染色体浓度"] = df["Y染色体浓度"].apply(clean_numeric)

# 第三步：去重
df = df.sort_values("检测孕周").drop_duplicates("孕妇代码", keep="first")

# 第四步：只删除真正的缺失值，保留有效数据
df = df.dropna(subset=["检测孕周", "孕妇BMI", "Y染色体浓度"])

#导出清洗后的数据到CSV
df.to_csv("清洗后_EDA数据集.csv", index=False, encoding="utf-8-sig")
print("2025国赛C题 第一问 探索性数据分析（EDA）")
print("="*60)
print(f"最终用于EDA的样本量：{len(df)} 行")

# 校验：如果样本量<100，直接报错提示
if len(df) < 100:
    print("样本量过少！请检查数据清洗逻辑！")
    exit()

# 1. 变量分布检查（直方图 + 箱线图）
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

# 直方图
df["检测孕周"].plot(kind="hist", bins=20, color='#4285F4', edgecolor='white', ax=axes[0,0])
axes[0,0].set_title("孕周分布")

df["孕妇BMI"].plot(kind="hist", bins=20, color='#34A853', edgecolor='white', ax=axes[0,1])
axes[0,1].set_title("BMI分布")

df["Y染色体浓度"].plot(kind="hist", bins=20, color='#FBBC05', edgecolor='white', ax=axes[0,2])
axes[0,2].set_title("Y染色体浓度分布")

# 箱线图
df["检测孕周"].plot(kind="box", vert=False, widths=0.7, ax=axes[1,0])
axes[1,0].set_title("孕周箱线图")

df["孕妇BMI"].plot(kind="box", vert=False, widths=0.7, ax=axes[1,1])
axes[1,1].set_title("BMI箱线图")

df["Y染色体浓度"].plot(kind="box", vert=False, widths=0.7, ax=axes[1,2])
axes[1,2].set_title("Y染色体浓度箱线图")

plt.tight_layout()
plt.savefig("5_变量分布检查.png", dpi=300, bbox_inches='tight')
plt.close()

#2. 单变量相关性分析（Pearson + Spearman）
# 提取变量
x1 = df["检测孕周"]
x2 = df["孕妇BMI"]
y  = df["Y染色体浓度"]

pairs = [
    ("孕周 & Y浓度", x1, y),
    ("BMI  & Y浓度", x2, y),
    ("孕周 & BMI  ", x1, x2)
]

rows = []
for name, a, b in pairs:
    pr, pp = pearsonr(a, b)
    sr, sp = spearmanr(a, b)
    sig = "显著" if pp < 0.05 else "不显著"
    rows.append({
        "变量对": name,
        "Pearson_r": round(pr,3),
        "Pearson_p": round(pp,4),
        "Spearman_r": round(sr,3),
        "Spearman_p": round(sp,4),
        "显著性": sig
    })

corr_df = pd.DataFrame(rows)
print(corr_df.to_string(index=False))

#导出相关性分析结果到CSV
corr_df.to_csv("相关性分析结果.csv", index=False, encoding="utf-8-sig")


# 热力图
plt.figure(figsize=(8,6))
sns.heatmap(df[["检测孕周","孕妇BMI","Y染色体浓度"]].corr(),
            annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("相关性热力图")
plt.tight_layout()
plt.savefig("2_相关性热力图.png", dpi=300)
plt.close()

#3. 可视化趋势分析（散点图 + 分组散点图）
# === 3.1 双变量散点图 + 拟合线 ===
fig, (ax1, ax2) = plt.subplots(1,2,figsize=(14,5))

# 孕周 vs Y
sns.regplot(x="检测孕周", y="Y染色体浓度", data=df, color='#4285F4', line_kws={"color":"red"}, ax=ax1)
ax1.set_title("孕周 → Y染色体浓度")
ax1.set_xlabel("检测孕周")
ax1.set_ylabel("Y染色体浓度")

# BMI vs Y
sns.regplot(x="孕妇BMI", y="Y染色体浓度", data=df, color='#34A853', line_kws={"color":"red"}, ax=ax2)
ax2.set_title("BMI → Y染色体浓度")
ax2.set_xlabel("孕妇BMI")
ax2.set_ylabel("Y染色体浓度")

plt.tight_layout()
plt.savefig("3_双变量趋势图.png", dpi=300)
plt.close()

# === 3.2 分组BMI散点图 ===
df["BMI分组"] = pd.cut(df["孕妇BMI"],
                      bins=[0,18.5,24,28,100],
                      labels=["低体重","正常","超重","肥胖"])

#导出带BMI分组的完整分析数据
df.to_csv("带BMI分组_EDA完整数据.csv", index=False, encoding="utf-8-sig")

plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x="检测孕周", y="Y染色体浓度", hue="BMI分组", palette="tab10", s=30)
sns.kdeplot(data=df, x="检测孕周", y="Y染色体浓度", levels=4, color='black', linestyles='--')
plt.title("孕周-Y浓度趋势（按BMI分组）")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("4_BMI分组趋势图.png", dpi=300)
plt.close()