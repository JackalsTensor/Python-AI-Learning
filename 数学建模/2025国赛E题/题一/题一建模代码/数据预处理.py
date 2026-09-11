import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
