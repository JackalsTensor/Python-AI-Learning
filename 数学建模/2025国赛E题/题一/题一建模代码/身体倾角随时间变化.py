import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ====================== 解决中文乱码 + 空白问题（必加） ======================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 100

# ========== 1. 读取数据 ==========
# 请替换成你的实际文件路径
df = pd.read_excel(r"D:\PythonProject1\数学建模\2025国赛E题\数据\运动者1的跳远位置信息.xlsx")

# ========== 2. 定义关键点编号（根据附件2 + 常识） ==========
# 17:左脚踝  18:右脚踝
# 21:左髋    22:右髋
# 5:左肩     6:右肩

# ========== 3. 提取关键点坐标 ==========
# 左脚踝
left_ankle_x = df['17_X']
left_ankle_y = df['17_Y']

# 右脚踝
right_ankle_x = df['18_X']
right_ankle_y = df['18_Y']

# 左髋
left_hip_x = df['21_X']
left_hip_y = df['21_Y']

# 右髋
right_hip_x = df['22_X']
right_hip_y = df['22_Y']

# 左肩
left_shoulder_x = df['5_X']
left_shoulder_y = df['5_Y']

# 右肩
right_shoulder_x = df['6_X']
right_shoulder_y = df['6_Y']

# 髋部中点（重心替代）
hip_center_y = (left_hip_y + right_hip_y) / 2
hip_center_x = (left_hip_x + right_hip_x) / 2

# 肩部中点
shoulder_center_y = (left_shoulder_y + right_shoulder_y) / 2
shoulder_center_x = (left_shoulder_x + right_shoulder_x) / 2

# ========== 4. 定义起跳帧和落地帧（根据你的检测结果） ==========
takeoff_frame = 16   # 你之前确定的起跳帧
landing_frame = 244   # 你之前确定的落地帧

frames = np.arange(len(df))

# 倾角计算：肩部中心 → 髋部中心 与水平夹角
dx = shoulder_center_x - hip_center_x
dy = shoulder_center_y - hip_center_y
angle = np.arctan2(dy, dx) * 180 / np.pi  # 转为度数

plt.figure(figsize=(12, 5))
plt.plot(frames, angle, 'g-', linewidth=1.5, label="身体倾角")

# 标注滞空区间
plt.axvspan(takeoff_frame, landing_frame, alpha=0.2, color='yellow', label='滞空阶段')

plt.xlabel('帧号', fontsize=12)
plt.ylabel('身体倾角 (度)', fontsize=12)
plt.title('运动者1 立定跳远 - 身体倾角变化曲线', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# ====================== 优化保存：无空白 + 高清 + 中文文件名 ======================
plt.savefig(
    '运动者1_身体倾角变化曲线.png',
    dpi=300,
    bbox_inches='tight',  # 自动切掉多余空白
    facecolor='white'     # 纯白背景
)

plt.show()
print("✅ 图片已保存：运动者1_身体倾角变化曲线.png")