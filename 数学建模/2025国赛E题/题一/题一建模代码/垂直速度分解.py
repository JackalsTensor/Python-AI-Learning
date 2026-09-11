import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ====================== 解决中文乱码 + 空格问题（核心） ======================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 100

# ========== 1. 读取数据 ==========
df = pd.read_excel(r"D:\PythonProject1\数学建模\2025国赛E题\数据\运动者1的跳远位置信息.xlsx")

# ========== 2. 定义关键点编号 ==========
# 17:左脚踝  18:右脚踝
# 21:左髋    22:右髋
# 5:左肩     6:右肩

# ========== 3. 提取关键点坐标 ==========
left_ankle_x = df['17_X']
left_ankle_y = df['17_Y']
right_ankle_x = df['18_X']
right_ankle_y = df['18_Y']

left_hip_x = df['21_X']
left_hip_y = df['21_Y']
right_hip_x = df['22_X']
right_hip_y = df['22_Y']

left_shoulder_x = df['5_X']
left_shoulder_y = df['5_Y']
right_shoulder_x = df['6_X']
right_shoulder_y = df['6_Y']

hip_center_y = (left_hip_y + right_hip_y) / 2
hip_center_x = (left_hip_x + right_hip_x) / 2

shoulder_center_y = (left_shoulder_y + right_shoulder_y) / 2
shoulder_center_x = (left_shoulder_x + right_shoulder_x) / 2

# ========== 4. 起跳、落地帧 ==========
takeoff_frame = 16
landing_frame = 244
frames = np.arange(len(df))

# ========== 速度计算 ==========
vx = np.zeros(len(df))
vy = np.zeros(len(df))

for i in range(1, len(df)-1):
    vx[i] = (hip_center_x[i+1] - hip_center_x[i-1]) / 2
    vy[i] = (hip_center_y[i+1] - hip_center_y[i-1]) / 2

start = max(0, takeoff_frame - 10)
end = min(len(df), takeoff_frame + 20)
frames_zoom = frames[start:end]

# ========== 绘图 ==========
plt.figure(figsize=(12, 5))
plt.plot(frames_zoom, vx[start:end], 'r-', linewidth=1.5, label='水平速度 vx')
plt.plot(frames_zoom, vy[start:end], 'b-', linewidth=1.5, label='垂直速度 vy')

plt.axvline(takeoff_frame, color='k', linestyle='--', linewidth=2, label='起跳时刻')
plt.axhline(0, color='gray', linestyle=':', linewidth=1)

plt.xlabel('帧号', fontsize=12)
plt.ylabel('速度 (像素/帧)', fontsize=12)
plt.title('运动者1 立定跳远 - 起跳前后速度分解', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# ====================== 保存图片（自动裁剪空白 + 高清） ======================
plt.savefig(
    '运动者1_起跳前后速度分解.png',  # 干净中文名
    dpi=300,
    bbox_inches='tight',  # 自动裁掉空白
    facecolor='white'
)

plt.show()

print("✅ 图片已保存：运动者1_起跳前后速度分解.png")