import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ====================== 解决中文乱码 + 空白问题（统一配置） ======================
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

def draw_stick_figure(ax, frame_data, title):
    """画单帧的火柴人姿态"""
    # 关键点坐标
    points = {
        'head': (frame_data['0_X'], frame_data['0_Y']),
        'neck': (frame_data['1_X'], frame_data['1_Y']),
        'LShoulder': (frame_data['5_X'], frame_data['5_Y']),
        'RShoulder': (frame_data['6_X'], frame_data['6_Y']),
        'LHip': (frame_data['21_X'], frame_data['21_Y']),
        'RHip': (frame_data['22_X'], frame_data['22_Y']),
        'LKnee': (frame_data['19_X'], frame_data['19_Y']),
        'RKnee': (frame_data['20_X'], frame_data['20_Y']),
        'LAnkle': (frame_data['17_X'], frame_data['17_Y']),
        'RAnkle': (frame_data['18_X'], frame_data['18_Y']),
    }

    # 连接关系
    connections = [
        ('head', 'neck'),
        ('neck', 'LShoulder'), ('neck', 'RShoulder'),
        ('LShoulder', 'LHip'), ('RShoulder', 'RHip'),
        ('LHip', 'RHip'),
        ('LHip', 'LKnee'), ('LKnee', 'LAnkle'),
        ('RHip', 'RKnee'), ('RKnee', 'RAnkle'),
    ]

    for (p1, p2) in connections:
        if p1 in points and p2 in points:
            x = [points[p1][0], points[p2][0]]
            y = [points[p1][1], points[p2][1]]
            ax.plot(x, y, 'k-', linewidth=2)

    # 画关键点
    for name, (x, y) in points.items():
        ax.plot(x, y, 'ro', markersize=4)

    ax.set_title(title)
    ax.set_aspect('equal')
    ax.invert_yaxis()  # 图像Y轴向下为正
    ax.axis('off')


# 选取三个典型时刻
frames_snapshot = [takeoff_frame + 10, (takeoff_frame + landing_frame) // 2, landing_frame - 10]
titles = ['起跳上升期', '腾空最高点附近', '落地前准备']

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for i, (frame, title) in enumerate(zip(frames_snapshot, titles)):
    draw_stick_figure(axes[i], df.iloc[frame], title)

plt.suptitle('运动者1 立定跳远 - 滞空阶段姿态序列', fontsize=14)
plt.tight_layout()

# ====================== 优化保存：无空白 + 高清 + 中文名称 ======================
plt.savefig(
    '运动者1_滞空阶段姿态序列.png',
    dpi=300,
    bbox_inches='tight',
    facecolor='white'
)

plt.show()
print("✅ 图片已保存：运动者1_滞空阶段姿态序列.png")