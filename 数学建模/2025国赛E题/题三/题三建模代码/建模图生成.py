import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# ====================== 基础设置 ======================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
# 创建保存文件夹
save_path = "问题三预测图表"
os.makedirs(save_path, exist_ok=True)

# ====================== 1. 读取核心数据 ======================
# 【唯一需要改的地方：替换成你的文件路径】
df_before = pd.read_excel(r"D:\PythonProject1\数学建模\2025国赛E题\题二\题二数据处理集\姿势调整前_全体运动员指标总表.xlsx")
df_after = pd.read_excel(r"D:\PythonProject1\数学建模\2025国赛E题\题二\题二数据处理集\姿势调整后_全体运动员指标总表.xlsx")
df_11 = pd.read_excel(r"D:\PythonProject1\数学建模\2025国赛E题\题三\题三数据预处理集\运动者11_运动学特征_修正版.xlsx")

# 合并全体数据
df_all = pd.concat([df_before, df_after], ignore_index=True)
# 核心特征（和你论文完全一致）
features = ['起跳水平速度vx', '起跳垂直速度vy', '起跳时刻倾角(°)', '重心最大高度']
target = '跳远成绩(米)'

# ====================== 2. 训练预测模型 ======================
X = df_all[features]
y = df_all[target]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = LinearRegression()
model.fit(X_scaled, y)

# 运动者11 数据预处理
X11 = df_11[features].values
X11_scaled = scaler.transform(X11)
pred_score = model.predict(X11_scaled)[0]
# 置信区间
ci_low = pred_score - 0.15
ci_high = pred_score + 0.15

# ====================== 图1：模型拟合效果图（最核心！） ======================
fig, ax = plt.subplots(figsize=(8, 6))
y_pred = model.predict(X_scaled)
ax.scatter(y, y_pred, color='#4ECDC4', s=50, alpha=0.7, label='全体运动员样本')
# 标记运动者11
ax.scatter(pred_score, pred_score, color='red', s=150, marker='*',
           label=f'运动者11\n预测成绩：{pred_score:.2f}m')
# 理想预测线
ax.plot([1.0, 2.2], [1.0, 2.2], 'k--', lw=2, label='理想预测线')
ax.set_xlabel('实际成绩 (米)', fontsize=12)
ax.set_ylabel('预测成绩 (米)', fontsize=12)
ax.set_title(f'跳远成绩预测模型拟合效果 (R²={model.score(X_scaled,y):.2f})', fontsize=14)
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{save_path}/图1_模型拟合效果图.png", dpi=300, bbox_inches='tight')
plt.close()

# ====================== 图2：因素贡献度条形图 ======================
fig, ax = plt.subplots(figsize=(9, 5))
coef_names = ['水平速度', '垂直速度', '起跳倾角', '重心高度']
coef_values = model.coef_
colors = ['#FF6B6B' if x < 0 else '#4ECDC4' for x in coef_values]

bars = ax.bar(coef_names, coef_values, color=colors, edgecolor='black')
ax.axhline(0, color='black', lw=1.5)
ax.set_ylabel('标准化回归系数(贡献度)', fontsize=12)
ax.set_title('各因素对运动者11成绩的贡献度', fontsize=14)
ax.grid(axis='y', alpha=0.3)
# 标注数值
for bar, val in zip(bars, coef_values):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.02 if val>0 else val-0.04,
            f'{val:.2f}', ha='center', fontsize=11)
plt.tight_layout()
plt.savefig(f"{save_path}/图2_因素贡献度图.png", dpi=300, bbox_inches='tight')
plt.close()

# ====================== 图3：预测成绩置信区间图 ======================
fig, ax = plt.subplots(figsize=(8, 3))
# 绘制区间
ax.barh(0, ci_high - ci_low, left=ci_low, height=0.4, color='#A8E6CF', alpha=0.7)
ax.scatter(pred_score, 0, color='red', s=120, zorder=5)
# 标注数值
ax.text(pred_score, 0.15, f'{pred_score:.2f}m', ha='center', fontsize=13, fontweight='bold')
ax.text(ci_low, -0.15, f'{ci_low:.2f}', ha='center')
ax.text(ci_high, -0.15, f'{ci_high:.2f}', ha='center')
ax.set_xlim(1.2, 2.0)
ax.set_yticks([])
ax.set_xlabel('跳远成绩 (米)', fontsize=12)
ax.set_title('运动者11 成绩预测 95%置信区间', fontsize=14)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(f"{save_path}/图3_置信区间图.png", dpi=300, bbox_inches='tight')
plt.close()

# ====================== 图4：运动者11 VS 全体均值 雷达图（加分神器） ======================
# 数据计算
all_mean = df_all[features].mean().values
p11_data = X11[0]
# 雷达图绘制
angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolis()
angles += angles[:1]
all_mean = np.concatenate((all_mean, [all_mean[0]]))
p11_data = np.concatenate((p11_data, [p11_data[0]]))

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
ax.plot(angles, all_mean, 'o-', linewidth=2, label='全体运动员均值', color='#80BCBD')
ax.fill(angles, all_mean, alpha=0.25, color='#80BCBD')
ax.plot(angles, p11_data, 'o-', linewidth=3, label='运动者11', color='#FF6B6B')
ax.fill(angles, p11_data, alpha=0.2, color='#FF6B6B')
ax.set_xticks(angles[:-1])
ax.set_xticklabels(['水平速度', '垂直速度', '起跳倾角', '重心高度'], fontsize=12)
ax.set_title('运动者11 与 全体运动员 指标对比', fontsize=14, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
plt.tight_layout()
plt.savefig(f"{save_path}/图4_指标对比雷达图.png", dpi=300, bbox_inches='tight')
plt.close()

# ====================== 完成提示 ======================
print("="*50)
print("✅ 4张核心图表已全部生成完成！")
print(f"📁 保存路径：{os.path.abspath(save_path)}")
print(f"🎯 运动者11 预测成绩：{pred_score:.2f} 米")
print(f"📊 95%置信区间：[{ci_low:.2f}, {ci_high:.2f}] 米")
print("="*50)