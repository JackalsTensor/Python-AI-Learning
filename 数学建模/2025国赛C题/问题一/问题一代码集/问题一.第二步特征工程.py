import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pickle

# ====================== 加载数据 ======================
df = pd.read_csv(r"/数学建模/2025国赛C题/问题一/问题一数据集/清洗后_EDA数据集.csv")

# ====================== 核心修正：孕周从天转成周 ======================
df["检测孕周_周"] = df["检测孕周"] / 7
print(f"孕周范围：{df['检测孕周_周'].min():.1f} ~ {df['检测孕周_周'].max():.1f} 周")
print(f"孕周均值：{df['检测孕周_周'].mean():.1f} 周")

# ====================== 1. 特征选择（扩充测序质量特征） ======================
# 核心：加入测序质量相关特征（提升R²的关键）
feature_cols = [
    "检测孕周_周",
    "孕妇BMI",
    "GC含量",
    "原始读段数",
    "唯一比对的读段数",
    "重复读段的比例",
    "在参考基因组上比对的比例"
]

# 检查特征列是否存在（避免KeyError）
for col in feature_cols:
    if col not in df.columns:
        raise ValueError(f"数据集中缺少特征列：{col}，请检查列名是否正确！")

X = df[feature_cols].copy()
y = df["Y染色体浓度"].copy()

# ====================== 2. 分层划分数据集（7:3，保持原逻辑） ======================
df["孕周分组"] = pd.qcut(df["检测孕周_周"], q=3, labels=["早", "中", "晚"])
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=df["孕周分组"]
)

# ====================== 3. 非线性特征构造（核心优化） ======================
# ① 平方项（捕捉非线性关系）
X_train["孕周平方"] = X_train["检测孕周_周"] ** 2
X_test["孕周平方"] = X_test["检测孕周_周"] ** 2

X_train["BMI平方"] = X_train["孕妇BMI"] ** 2
X_test["BMI平方"] = X_test["孕妇BMI"] ** 2

# ② 交互项（捕捉孕周与BMI的协同效应）
X_train["孕周_BMI交互"] = X_train["检测孕周_周"] * X_train["孕妇BMI"]
X_test["孕周_BMI交互"] = X_test["检测孕周_周"] * X_test["孕妇BMI"]

# ====================== 4. 特征中心化（避免量纲问题，仅对基础特征） ======================
# 仅用训练集均值中心化（无数据泄露）
ga_mean = X_train["检测孕周_周"].mean()
bmi_mean = X_train["孕妇BMI"].mean()

X_train["检测孕周_周_中心化"] = X_train["检测孕周_周"] - ga_mean
X_test["检测孕周_周_中心化"] = X_test["检测孕周_周"] - ga_mean

X_train["孕妇BMI_中心化"] = X_train["孕妇BMI"] - bmi_mean
X_test["孕妇BMI_中心化"] = X_test["孕妇BMI"] - bmi_mean

# ====================== 5. 最终特征集（整合所有特征） ======================
final_features = [
    # 中心化基础特征
    "检测孕周_周_中心化",
    "孕妇BMI_中心化",
    # 测序质量特征
    "GC含量",
    "原始读段数",
    "唯一比对的读段数",
    "重复读段的比例",
    "在参考基因组上比对的比例",
    # 非线性特征
    "孕周平方",
    "BMI平方",
    "孕周_BMI交互"
]

X_train_final = X_train[final_features].copy()
X_test_final = X_test[final_features].copy()

# ====================== 6. VIF共线性检查（关键：避免过拟合） ======================
def calculate_vif(df, features):
    """计算VIF值，检查共线性（VIF<10为可接受）"""
    vif_data = pd.DataFrame()
    vif_data["特征"] = features
    vif_data["VIF"] = [variance_inflation_factor(df[features].values, i) for i in range(len(features))]
    return vif_data

vif_result = calculate_vif(X_train_final, final_features)
print("\n📊 VIF共线性检查结果：")
print(vif_result.sort_values(by="VIF", ascending=False))

# ====================== 7. 保存结果 ======================
# 保存特征矩阵
X_train_final.to_csv("训练集_最终特征_扩充版.csv", index=False)
X_test_final.to_csv("验证集_最终特征_扩充版.csv", index=False)
y_train.to_csv("y_train_扩充版.csv", index=False)
y_test.to_csv("y_test_扩充版.csv", index=False)

# 保存特征工程参数（用于后续复用）
feat_eng_params = {
    "ga_mean": ga_mean,
    "bmi_mean": bmi_mean,
    "final_features": final_features,
    "unit": "周",
    "vif_result": vif_result.to_dict()
}
with open("特征工程参数_扩充版.pkl", "wb") as f:
    pickle.dump(feat_eng_params, f)

# ====================== 输出关键信息 ======================
print("\n✅ 特征工程（扩充版）完成！")
print(f"训练集特征形状：{X_train_final.shape}")
print(f"验证集特征形状：{X_test_final.shape}")
print("\n📌 最终特征列表：")
for i, feat in enumerate(final_features, 1):
    print(f"{i}. {feat}")
print("\n📌 中心化特征范围：")
print(f"训练集-孕周中心化：{X_train_final['检测孕周_周_中心化'].min():.2f} ~ {X_train_final['检测孕周_周_中心化'].max():.2f}")
print(f"验证集-孕周中心化：{X_test_final['检测孕周_周_中心化'].min():.2f} ~ {X_test_final['检测孕周_周_中心化'].max():.2f}")