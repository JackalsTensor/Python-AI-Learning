import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import r2_score, mean_squared_error

# ====================== 全局设置（论文级可视化） ======================
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 150
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8

# ====================== 1. 加载真实数据 ======================
X_train = pd.read_csv(r"/数学建模/2025国赛C题/问题一/问题一数据集/训练集_最终特征.csv")
X_val = pd.read_csv(r"/数学建模/2025国赛C题/问题一/问题一数据集/验证集_最终特征.csv")
y_train = pd.read_csv(r"/数学建模/2025国赛C题/问题一/问题一数据集/y_train.csv").iloc[:, 0]
y_val = pd.read_csv(r"/数学建模/2025国赛C题/问题一/问题一数据集/y_test.csv").iloc[:, 0]

# ====================== 2. 训练3个模型 ======================
# 模型1：基础线性
X1_train = sm.add_constant(X_train[["孕周_中心化", "孕妇BMI"]])
X1_val = sm.add_constant(X_val[["孕周_中心化", "孕妇BMI"]])
model1 = sm.OLS(y_train, X1_train).fit(cov_type="HC3")
y_pred1 = model1.predict(X1_val)

# 模型2：加二次项
X2_train = X1_train.copy()
X2_train["孕周_二次项"] = X_train["孕周_中心化"] ** 2
X2_val = X1_val.copy()
X2_val["孕周_二次项"] = X_val["孕周_中心化"] ** 2
model2 = sm.OLS(y_train, X2_train).fit(cov_type="HC3")
y_pred2 = model2.predict(X2_val)

# 模型3：加交互项
X3_train = X2_train.copy()
X3_train["交互_孕周×BMI"] = X_train["孕周_中心化"] * X_train["孕妇BMI"]
X3_val = X2_val.copy()
X3_val["交互_孕周×BMI"] = X_val["孕周_中心化"] * X_val["孕妇BMI"]
model3 = sm.OLS(y_train, X3_train).fit(cov_type="HC3")
y_pred3 = model3.predict(X3_val)

# ====================== 3. 图1：预测值vs真实值对比图（核心图） ======================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 模型1
axes[0].scatter(y_val, y_pred1, alpha=0.6, color='#4285F4', s=30)
axes[0].plot([y_val.min(), y_val.max()], [y_val.min(), y_val.max()], 'r--', lw=2)
axes[0].set_title(f"模型1（基础线性）\nR²={r2_score(y_val, y_pred1):.4f}, RMSE={np.sqrt(mean_squared_error(y_val, y_pred1)):.4f}")
axes[0].set_xlabel("真实Y染色体浓度")
axes[0].set_ylabel("预测Y染色体浓度")
axes[0].grid(alpha=0.3)

# 模型2
axes[1].scatter(y_val, y_pred2, alpha=0.6, color='#EA4335', s=30)
axes[1].plot([y_val.min(), y_val.max()], [y_val.min(), y_val.max()], 'r--', lw=2)
axes[1].set_title(f"模型2（加二次项）\nR²={r2_score(y_val, y_pred2):.4f}, RMSE={np.sqrt(mean_squared_error(y_val, y_pred2)):.4f}")
axes[1].set_xlabel("真实Y染色体浓度")
axes[1].set_ylabel("预测Y染色体浓度")
axes[1].grid(alpha=0.3)

# 模型3
axes[2].scatter(y_val, y_pred3, alpha=0.6, color='#34A853', s=30)
axes[2].plot([y_val.min(), y_val.max()], [y_val.min(), y_val.max()], 'r--', lw=2)
axes[2].set_title(f"模型3（加交互项）\nR²={r2_score(y_val, y_pred3):.4f}, RMSE={np.sqrt(mean_squared_error(y_val, y_pred3)):.4f}")
axes[2].set_xlabel("真实Y染色体浓度")
axes[2].set_ylabel("预测Y染色体浓度")
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("1_预测值vs真实值对比.png", dpi=300, bbox_inches='tight')
plt.close()

# ====================== 4. 图2：残差分布对比图 ======================
resid1 = y_val - y_pred1
resid2 = y_val - y_pred2
resid3 = y_val - y_pred3

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# 模型1
axes[0].hist(resid1, bins=20, alpha=0.7, color='#4285F4', edgecolor='black')
axes[0].axvline(0, color='red', linestyle='--')
axes[0].set_title(f"模型1 残差分布\n均值={resid1.mean():.4f}, 标准差={resid1.std():.4f}")
axes[0].set_xlabel("残差（真实值-预测值）")
axes[0].set_ylabel("频数")
axes[0].grid(alpha=0.3)

# 模型2
axes[1].hist(resid2, bins=20, alpha=0.7, color='#EA4335', edgecolor='black')
axes[1].axvline(0, color='red', linestyle='--')
axes[1].set_title(f"模型2 残差分布\n均值={resid2.mean():.4f}, 标准差={resid2.std():.4f}")
axes[1].set_xlabel("残差（真实值-预测值）")
axes[1].set_ylabel("频数")
axes[1].grid(alpha=0.3)

# 模型3
axes[2].hist(resid3, bins=20, alpha=0.7, color='#34A853', edgecolor='black')
axes[2].axvline(0, color='red', linestyle='--')
axes[2].set_title(f"模型3 残差分布\n均值={resid3.mean():.4f}, 标准差={resid3.std():.4f}")
axes[2].set_xlabel("残差（真实值-预测值）")
axes[2].set_ylabel("频数")
axes[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("6_残差分布对比.png", dpi=300, bbox_inches='tight')
plt.close()

# ====================== 5. 图3：孕周拟合曲线对比图 ======================
# 固定BMI为均值，绘制孕周-Y浓度拟合曲线
bmi_mean = X_train["孕妇BMI"].mean()
week_range = np.linspace(X_train["孕周_中心化"].min(), X_train["孕周_中心化"].max(), 100)

# 模型1拟合线
y_fit1 = model1.params["const"] + model1.params["孕周_中心化"] * week_range + model1.params["孕妇BMI"] * bmi_mean

# 模型2拟合线
y_fit2 = model2.params["const"] + model2.params["孕周_中心化"] * week_range + model2.params["孕妇BMI"] * bmi_mean + model2.params["孕周_二次项"] * (week_range ** 2)

# 模型3拟合线
y_fit3 = model3.params["const"] + model3.params["孕周_中心化"] * week_range + model3.params["孕妇BMI"] * bmi_mean + model3.params["孕周_二次项"] * (week_range ** 2) + model3.params["交互_孕周×BMI"] * week_range * bmi_mean

plt.figure(figsize=(10, 6))
plt.plot(week_range, y_fit1, label="模型1（基础线性）", color='#4285F4', lw=2)
plt.plot(week_range, y_fit2, label="模型2（加二次项）", color='#EA4335', lw=2, linestyle='--')
plt.plot(week_range, y_fit3, label="模型3（加交互项）", color='#34A853', lw=2, linestyle=':')
plt.scatter(X_val["孕周_中心化"], y_val, alpha=0.5, color='#9AA0A6', s=30, label="验证集真实样本")
plt.title("固定BMI均值下，孕周-Y浓度拟合曲线对比")
plt.xlabel("中心化孕周")
plt.ylabel("Y染色体浓度")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("7_孕周拟合曲线对比.png", dpi=300, bbox_inches='tight')
plt.close()

# ====================== 6. 图4：模型性能雷达图 ======================
# 提取性能指标
metrics = ["训练集调整R²", "验证集R²", "RMSE", "AIC", "BIC"]
model1_scores = [model1.rsquared_adj, r2_score(y_val, y_pred1), 1/np.sqrt(mean_squared_error(y_val, y_pred1)), 1/model1.aic, 1/model1.bic]
model2_scores = [model2.rsquared_adj, r2_score(y_val, y_pred2), 1/np.sqrt(mean_squared_error(y_val, y_pred2)), 1/model2.aic, 1/model2.bic]
model3_scores = [model3.rsquared_adj, r2_score(y_val, y_pred3), 1/np.sqrt(mean_squared_error(y_val, y_pred3)), 1/model3.aic, 1/model3.bic]

# 归一化到0-1区间
def normalize(scores):
    min_s = min(scores)
    max_s = max(scores)
    return [(s - min_s)/(max_s - min_s) for s in scores]

model1_norm = normalize(model1_scores)
model2_norm = normalize(model2_scores)
model3_norm = normalize(model3_scores)

# 雷达图绘制
angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]

model1_norm += model1_norm[:1]
model2_norm += model2_norm[:1]
model3_norm += model3_norm[:1]
metrics += metrics[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.plot(angles, model1_norm, label="模型1（基础线性）", color='#4285F4', lw=2)
ax.fill(angles, model1_norm, color='#4285F4', alpha=0.25)
ax.plot(angles, model2_norm, label="模型2（加二次项）", color='#EA4335', lw=2)
ax.fill(angles, model2_norm, color='#EA4335', alpha=0.25)
ax.plot(angles, model3_norm, label="模型3（加交互项）", color='#34A853', lw=2)
ax.fill(angles, model3_norm, color='#34A853', alpha=0.25)
ax.set_thetagrids(np.degrees(angles[:-1]), metrics[:-1])
ax.set_title("三个模型综合性能雷达图（归一化）", y=1.1)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
plt.savefig("8_模型性能雷达图.png", dpi=300, bbox_inches='tight')
plt.close()

print("✅ 4张对比图全部生成完成！")
print("📁 已生成：")
print("  1. 1_预测值vs真实值对比.png")
print("  2. 6_残差分布对比.png")
print("  3. 7_孕周拟合曲线对比.png")
print("  4. 8_模型性能雷达图.png")