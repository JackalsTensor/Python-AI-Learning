import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# ====================== 1. 读取你已经生成好的真实数据 ======================
X_train = pd.read_csv(r"/数学建模/2025国赛C题/问题一/问题一数据集/训练集_最终特征.csv")
y_train = pd.read_csv(r"/数学建模/2025国赛C题/问题一/问题一数据集/y_train.csv").iloc[:, 0]
X_test = pd.read_csv(r"/数学建模/2025国赛C题/问题一/问题一数据集/验证集_最终特征.csv")
y_test = pd.read_csv(r"/数学建模/2025国赛C题/问题一/问题一数据集/y_test.csv").iloc[:, 0]

# ====================== 2. 构建3个模型的特征 ======================
# 模型1：基础线性（中心化孕周 + BMI）
X1_train = sm.add_constant(X_train[["孕周_中心化", "孕妇BMI"]])
X1_test = sm.add_constant(X_test[["孕周_中心化", "孕妇BMI"]])

# 模型2：加二次项（中心化孕周 + BMI + 孕周二次项）
X2_train = X_train.copy()
X2_train["孕周_二次项"] = X2_train["孕周_中心化"] ** 2
X2_train = sm.add_constant(X2_train)
X2_test = X_test.copy()
X2_test["孕周_二次项"] = X2_test["孕周_中心化"] ** 2
X2_test = sm.add_constant(X2_test)

# 模型3：加交互项（中心化孕周 + BMI + 孕周二次项 + 交互项）
X3_train = X2_train.copy()
X3_train["交互_孕周×BMI"] = X3_train["孕周_中心化"] * X3_train["孕妇BMI"]
X3_test = X2_test.copy()
X3_test["交互_孕周×BMI"] = X3_test["孕周_中心化"] * X3_test["孕妇BMI"]


# ====================== 3. 训练3个模型，计算所有指标 ======================
def train_and_evaluate(model_name, X_train, y_train, X_test, y_test):
    # 训练模型（HC3稳健标准误）
    model = sm.OLS(y_train, X_train).fit(cov_type="HC3")

    # 计算训练集指标
    adj_r2 = model.rsquared_adj.round(4)
    aic = model.aic.round(2)
    bic = model.bic.round(2)
    f_pvalue = model.f_pvalue
    max_vif = max([variance_inflation_factor(X_train.values, i) for i in range(X_train.shape[1])]).round(2)

    # 计算验证集指标
    y_pred = model.predict(X_test)
    test_r2 = (1 - ((y_test - y_pred) ** 2).sum() / ((y_test - y_test.mean()) ** 2).sum()).round(4)
    test_rmse = ((y_test - y_pred) ** 2).mean() ** 0.5

    # 输出核心结果
    print("=" * 60)
    print(f"【{model_name}】")
    print("=" * 60)
    print(f"训练集调整R²：{adj_r2}")
    print(f"AIC：{aic}")
    print(f"BIC：{bic}")
    print(f"F检验p值：{f_pvalue:.4e}")
    print(f"验证集R²：{test_r2}")
    print(f"验证集RMSE：{test_rmse:.4f}")
    print(f"最大VIF：{max_vif}")
    print("\n回归系数表：")
    print(model.summary().tables[1])

    return {
        "模型名称": model_name,
        "训练集调整R²": adj_r2,
        "AIC": aic,
        "BIC": bic,
        "F检验p值": f_pvalue,
        "验证集R²": test_r2,
        "验证集RMSE": test_rmse,
        "最大VIF": max_vif
    }


# 依次训练3个模型
results = []
results.append(train_and_evaluate("模型1（基础线性）", X1_train, y_train, X1_test, y_test))
results.append(train_and_evaluate("模型2（加二次项）", X2_train, y_train, X2_test, y_test))
results.append(train_and_evaluate("模型3（加交互项）", X3_train, y_train, X3_test, y_test))

# ====================== 4. 生成最终对比表 ======================
print("\n" + "=" * 80)
print("【3个模型最终对比表】")
print("=" * 80)
result_df = pd.DataFrame(results)
print(result_df.to_string(index=False))

# 保存结果到CSV，直接复制进论文
result_df.to_csv("3个模型对比结果.csv", index=False, encoding="utf-8-sig")
print("\n✅ 结果已保存到：3个模型对比结果.csv")