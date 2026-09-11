import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ====================== 基础设置 ======================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
# 创建保存文件夹
save_path = "问题四训练建议图表"
os.makedirs(save_path, exist_ok=True)

# ====================== 核心数据（和论文完全一致） ======================
# 训练前后指标
features = ['起跳水平速度', '起跳垂直速度', '起跳倾角', '重心高度']
before_train = [11.00, 22.67, -16.10, 512.74]
after_train = [11.00, 22.67, -65.00, 530.00]

# 成绩提升贡献度
contribution_labels = ['起跳角度优化', '腾空高度提升']
contribution_values = [0.12, 0.04]
contribution_percent = ['75%', '25%']

# ====================== 图1：训练前后核心指标对比雷达图（必做） ======================
# 数据归一化（解决不同指标量级差异问题）
def normalize(data):
    return (np.array(data) - np.min(data)) / (np.max(data) - np.min(data))

before_norm = normalize(before_train)
after_norm = normalize(after_train)

# 雷达图绘制
angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolist()
angles += angles[:1]
before_norm = np.concatenate((before_norm, [before_norm[0]]))
after_norm = np.concatenate((after_norm, [after_norm[0]]))

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
ax.plot(angles, before_norm, 'o-', linewidth=2, label='训练前', color='#4ECDC4')
ax.fill(angles, before_norm, alpha=0.25, color='#4ECDC4')
ax.plot(angles, after_norm, 'o-', linewidth=3, label='训练后预期', color='#FF6B6B')
ax.fill(angles, after_norm, alpha=0.2, color='#FF6B6B')
ax.set_xticks(angles[:-1])
ax.set_xticklabels(features, fontsize=12)
ax.set_yticks([])  # 隐藏刻度，只看相对对比
ax.set_title('运动者11 训练前后核心技术指标对比', fontsize=14, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
plt.tight_layout()
plt.savefig(f"{save_path}/图1_训练前后指标对比雷达图.png", dpi=300, bbox_inches='tight')
plt.close()

# ====================== 图2：成绩提升贡献度分解图（必做） ======================
fig, ax = plt.subplots(figsize=(8, 4))
# 绘制堆积条形图
bars = ax.barh(0, contribution_values, left=[0, contribution_values[0]],
               color=['#FF6B6B', '#4ECDC4'], edgecolor='black', height=0.4)
# 标注数值和百分比
for bar, val, percent in zip(bars, contribution_values, contribution_percent):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}m\n({percent})', ha='center', va='center', fontsize=12, color='white', fontweight='bold')
ax.set_xlim(0, 0.18)
ax.set_yticks([])
ax.set_xlabel('成绩提升幅度 (米)', fontsize=12)
ax.set_title('短期训练后成绩提升贡献度分解', fontsize=14)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(f"{save_path}/图2_成绩提升贡献度分解图.png", dpi=300, bbox_inches='tight')
plt.close()

# ====================== 图3：2周针对性训练计划甘特图（加分） ======================
fig, ax = plt.subplots(figsize=(10, 6))
# 训练计划数据
tasks = [
    ('爆发力维持训练', 0, 14, '#A8E6CF'),
    ('落地姿势优化训练', 3, 14, '#88D8B0'),
    ('腾空高度提升训练', 0, 14, '#FFAAA5'),
    ('起跳角度纠正训练', 0, 14, '#FF8B94')
]
# 绘制甘特图
for i, (task, start, end, color) in enumerate(tasks):
    ax.barh(i, end - start, left=start, height=0.6, color=color, edgecolor='black')
    ax.text(start + (end - start)/2, i, task, ha='center', va='center', fontsize=11, fontweight='bold')
# 设置坐标轴
ax.set_yticks(range(len(tasks)))
ax.set_yticklabels([t[0] for t in tasks])
ax.set_xlabel('训练天数', fontsize=12)
ax.set_xlim(0, 14)
ax.set_xticks(range(0, 15, 2))
ax.set_title('运动者11 2周针对性训练计划', fontsize=14)
ax.grid(axis='x', alpha=0.3)
# 添加训练时长说明
ax.text(7, -0.8, '注：每天训练15-20分钟，每周训练4次', ha='center', fontsize=10, color='gray')
plt.tight_layout()
plt.savefig(f"{save_path}/图3_2周训练计划甘特图.png", dpi=300, bbox_inches='tight')
plt.close()

# ====================== 完成提示 ======================
print("="*50)
print("✅ 问题4 3张核心图表已全部生成完成！")
print(f"📁 保存路径：{os.path.abspath(save_path)}")
print("📊 生成图表：")
print("   1. 图1_训练前后指标对比雷达图.png")
print("   2. 图2_成绩提升贡献度分解图.png")
print("   3. 图3_2周训练计划甘特图.png")
print("="*50)