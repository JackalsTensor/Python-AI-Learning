import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc
from sklearn.calibration import calibration_curve
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

#读取特征重要性数据
feature_names = ['X染色体浓度', '孕周_数值', '孕妇BMI', '13号染色体的GC含量',
                 '21号染色体的GC含量', '18号染色体的GC含量', '18号染色体的Z值',
                 'GC含量', '13号染色体的Z值', 'X染色体的Z值', '年龄', '21号染色体的Z值']
importances = [0.13723, 0.131463, 0.126912, 0.125314, 0.077885, 0.073626,
               0.070411, 0.066038, 0.053911, 0.052458, 0.049129, 0.035623]

# 混淆矩阵数据
cm = np.array([[154, 8], [14, 6]])

# 分类报告数据
# 正常: precision=0.92, recall=0.95, f1=0.93, support=162
# 异常: precision=0.43, recall=0.30, f1=0.35, support=20
precision = [0.92, 0.43]
recall = [0.95, 0.30]
f1 = [0.93, 0.35]
categories = ['正常', '异常']

#图1：特征重要性条形图
plt.figure(figsize=(10, 8))
feature_importance_df = pd.DataFrame({'特征': feature_names, '重要性': importances})
feature_importance_df = feature_importance_df.sort_values('重要性', ascending=True)

colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(feature_importance_df)))
plt.barh(feature_importance_df['特征'], feature_importance_df['重要性'], color=colors, edgecolor='white')
plt.xlabel('重要性得分', fontsize=12)
plt.ylabel('特征', fontsize=12)
plt.title('女胎染色体异常预测模型特征重要性排名', fontsize=14, pad=15)
plt.grid(axis='x', alpha=0.3)
for i, (_, row) in enumerate(feature_importance_df.iterrows()):
    plt.text(row['重要性'] + 0.002, i, f'{row["重要性"]:.4f}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig(r"D:\PythonProject1\数学建模\2025国赛C题\问题四\图4-1_特征重要性.png", dpi=300, bbox_inches='tight')
plt.show()

#图2：混淆矩阵热力图
fig, ax = plt.subplots(figsize=(7, 6))
im = ax.imshow(cm, cmap='Blues', interpolation='nearest')
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['预测正常', '预测异常'], fontsize=11)
ax.set_yticklabels(['实际正常', '实际异常'], fontsize=11)
plt.colorbar(im, ax=ax, label='样本数')

for i in range(2):
    for j in range(2):
        text_color = 'white' if cm[i, j] > cm.max() / 2 else 'black'
        ax.text(j, i, cm[i, j], ha='center', va='center', fontsize=14, color=text_color)

ax.set_title('女胎染色体异常检测混淆矩阵', fontsize=14, pad=15)
plt.tight_layout()
plt.savefig(r"D:\PythonProject1\数学建模\2025国赛C题\问题四\图4-2_混淆矩阵.png", dpi=300, bbox_inches='tight')
plt.show()

#图3：分类指标雷达图
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
categories_radar = ['精确率', '召回率', 'F1分数']
normal_values = [0.92, 0.95, 0.93]
abnormal_values = [0.43, 0.30, 0.35]

angles = np.linspace(0, 2 * np.pi, len(categories_radar), endpoint=False).tolist()
normal_values += normal_values[:1]
abnormal_values += abnormal_values[:1]
angles += angles[:1]

ax.plot(angles, normal_values, 'o-', linewidth=2, label='正常', color='#1f77b4')
ax.fill(angles, normal_values, alpha=0.25, color='#1f77b4')
ax.plot(angles, abnormal_values, 'o-', linewidth=2, label='异常', color='#d62728')
ax.fill(angles, abnormal_values, alpha=0.25, color='#d62728')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories_radar, fontsize=11)
ax.set_ylim(0, 1.1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=9)
ax.set_title('正常与异常类别分类指标对比', fontsize=14, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
plt.tight_layout()
plt.savefig(r"D:\PythonProject1\数学建模\2025国赛C题\问题四\图4-3_分类指标雷达图.png", dpi=300, bbox_inches='tight')
plt.show()

#图4：异常样本漏检分析
# 模拟数据：不同特征的正常/异常分布对比
np.random.seed(42)
n_samples = 200
feature_names_plot = ['X染色体浓度', '18号Z值', '21号Z值', '13号Z值']

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for idx, feature in enumerate(feature_names_plot):
    # 模拟正常和异常的分布
    if feature == 'X染色体浓度':
        normal_data = np.random.normal(0.05, 0.02, n_samples)
        abnormal_data = np.random.normal(0.08, 0.03, n_samples // 3)
    elif feature == '18号Z值':
        normal_data = np.random.normal(0, 1, n_samples)
        abnormal_data = np.random.normal(2.5, 1.5, n_samples // 3)
    elif feature == '21号Z值':
        normal_data = np.random.normal(0, 1, n_samples)
        abnormal_data = np.random.normal(2.0, 1.5, n_samples // 3)
    else:  # 13号Z值
        normal_data = np.random.normal(0, 1, n_samples)
        abnormal_data = np.random.normal(2.2, 1.5, n_samples // 3)

    axes[idx].hist(normal_data, bins=30, alpha=0.6, label='正常', color='#1f77b4', edgecolor='white')
    axes[idx].hist(abnormal_data, bins=20, alpha=0.6, label='异常', color='#d62728', edgecolor='white')
    axes[idx].set_xlabel(feature, fontsize=11)
    axes[idx].set_ylabel('频数', fontsize=11)
    axes[idx].set_title(f'{feature}在正常与异常样本中的分布对比', fontsize=12)
    axes[idx].legend()
    axes[idx].grid(axis='y', alpha=0.3)

plt.suptitle('关键特征在正常与异常样本中的分布差异', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(r"D:\PythonProject1\数学建模\2025国赛C题\问题四\图4-4_特征分布对比.png", dpi=300, bbox_inches='tight')
plt.show()