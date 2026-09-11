import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ====================== 1. 解决中文乱码（必加） ======================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ====================== 2. 改成你自己的Excel文件绝对路径 ======================
# 姿势调整前总表路径
path_before = r"D:\PythonProject1\数学建模\2025国赛E题\题二\题二数据处理集\姿势调整前_全体运动员指标总表.xlsx"
# 姿势调整后总表路径
path_after = r"D:\PythonProject1\数学建模\2025国赛E题\题二\题二数据处理集\姿势调整后_全体运动员指标总表.xlsx"

# 读取数据
df_before = pd.read_excel(path_before)
df_after = pd.read_excel(path_after)

# ====================== 3. 图片保存文件夹（自动创建，保存在代码同级） ======================
save_dir = "问题二_6张对比图"
os.makedirs(save_dir, exist_ok=True)

# 统一保存函数
def save_plot(fig, name):
    full_path = os.path.join(save_dir, name)
    plt.tight_layout()
    fig.savefig(full_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"✅ 已生成：{name}")

# ==============================================================================
# 图1：纠正前后成绩对比箱线图
# ==============================================================================
fig, ax = plt.subplots(figsize=(6, 6))
data = [df_before['跳远成绩(米)'], df_after['跳远成绩(米)']]
box = ax.boxplot(data, labels=['姿势调整前', '姿势调整后'], patch_artist=True)
# 给箱子上色
colors = ['#FF6B6B', '#4ECDC4']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
# 加散点
ax.scatter(np.ones(len(df_before))*1, df_before['跳远成绩(米)'], color='black', alpha=0.5, s=20)
ax.scatter(np.ones(len(df_after))*2, df_after['跳远成绩(米)'], color='black', alpha=0.5, s=20)

ax.set_ylabel('跳远成绩（米）', fontsize=12)
ax.set_title('姿势纠正前后跳远成绩对比', fontsize=14)
ax.grid(axis='y', alpha=0.3)
save_plot(fig, "图1_纠正前后成绩对比箱线图.png")

# ==============================================================================
# 图2：纠正前后起跳速度对比（双指标）
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
# 左图：水平速度
data_vx = [df_before['起跳水平速度vx'], df_after['起跳水平速度vx']]
box_vx = axes[0].boxplot(data_vx, labels=['调整前', '调整后'], patch_artist=True)
for patch, color in zip(box_vx['boxes'], colors):
    patch.set_facecolor(color)
axes[0].set_ylabel('起跳水平速度（像素/帧）', fontsize=12)
axes[0].set_title('起跳水平速度对比', fontsize=12)
axes[0].grid(axis='y', alpha=0.3)

# 右图：垂直速度
data_vy = [df_before['起跳垂直速度vy'], df_after['起跳垂直速度vy']]
box_vy = axes[1].boxplot(data_vy, labels=['调整前', '调整后'], patch_artist=True)
for patch, color in zip(box_vy['boxes'], colors):
    patch.set_facecolor(color)
axes[1].set_ylabel('起跳垂直速度（像素/帧）', fontsize=12)
axes[1].set_title('起跳垂直速度对比', fontsize=12)
axes[1].grid(axis='y', alpha=0.3)

save_plot(fig, "图2_纠正前后起跳速度对比.png")

# ==============================================================================
# 图3：起跳角度与成绩的散点图（分阶段着色）
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
# 调整前
ax.scatter(df_before['起跳时刻倾角(°)'], df_before['跳远成绩(米)'],
           c='#FF6B6B', label='姿势调整前', s=80, alpha=0.7, edgecolors='black')
# 调整后
ax.scatter(df_after['起跳时刻倾角(°)'], df_after['跳远成绩(米)'],
           c='#4ECDC4', label='姿势调整后', s=80, alpha=0.7, edgecolors='black')

ax.set_xlabel('起跳时刻身体倾角（度）', fontsize=12)
ax.set_ylabel('跳远成绩（米）', fontsize=12)
ax.set_title('起跳倾角与跳远成绩的关系', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
save_plot(fig, "图3_起跳角度与成绩散点图.png")

# ==============================================================================
# 图4：重心最大高度与成绩的关系
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
# 调整前
ax.scatter(df_before['重心最大高度'], df_before['跳远成绩(米)'],
           c='#FF6B6B', label='姿势调整前', s=80, alpha=0.7, edgecolors='black')
# 调整后
ax.scatter(df_after['重心最大高度'], df_after['跳远成绩(米)'],
           c='#4ECDC4', label='姿势调整后', s=80, alpha=0.7, edgecolors='black')

ax.set_xlabel('重心最大高度（像素）', fontsize=12)
ax.set_ylabel('跳远成绩（米）', fontsize=12)
ax.set_title('重心最大高度与跳远成绩的关系', fontsize=14)
ax.legend()
ax.grid(True, alpha=0.3)
save_plot(fig, "图4_重心高度与成绩散点图.png")

# ==============================================================================
# 图5：核心指标均值对比柱状图
# ==============================================================================
metrics = ['起跳水平速度vx', '起跳垂直速度vy', '起跳时刻倾角(°)', '重心最大高度']
before_mean = [df_before[m].mean() for m in metrics]
after_mean = [df_after[m].mean() for m in metrics]

x = np.arange(len(metrics))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - width/2, before_mean, width, label='姿势调整前', color='#FF6B6B')
ax.bar(x + width/2, after_mean, width, label='姿势调整后', color='#4ECDC4')

ax.set_title('姿势调整前后核心运动学指标对比', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(metrics, rotation=10)
ax.legend()
ax.grid(axis='y', alpha=0.3)
save_plot(fig, "图5_核心指标均值对比.png")

# ==============================================================================
# 图6：成绩提升幅度分布直方图
# ==============================================================================
# 合并前后数据，计算提升幅度
df_before['阶段'] = '姿势调整前'
df_after['阶段'] = '姿势调整后'
df_all = pd.concat([df_before, df_after], ignore_index=True)

fig, ax = plt.subplots(figsize=(8, 5))
sns_colors = {'姿势调整前': '#FF6B6B', '姿势调整后': '#4ECDC4'}
for phase, color in sns_colors.items():
    subset = df_all[df_all['阶段'] == phase]
    ax.hist(subset['跳远成绩(米)'], alpha=0.5, label=phase, bins=5, color=color, edgecolor='black')

ax.set_xlabel('跳远成绩（米）', fontsize=12)
ax.set_ylabel('频次', fontsize=12)
ax.set_title('姿势调整前后成绩分布对比', fontsize=14)
ax.legend()
ax.grid(axis='y', alpha=0.3)
save_plot(fig, "图6_成绩分布直方图.png")

# ==============================================================================
print("\n🎉 全部 6 张图生成完成！")
print(f"📁 图片保存在：{os.path.abspath(save_dir)} 文件夹")