import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ====================== 【新增：解决中文乱码的核心配置】 ======================
# 强制设置支持中文的字体，彻底解决方框乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']  # 兼容Windows/Mac
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示异常
plt.rcParams['figure.dpi'] = 100  # 屏幕显示清晰度

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

# ========== 5. 绘图部分 ==========
plt.figure(figsize=(14, 6))  # 稍微加宽画布，避免文字拥挤
plt.plot(frames, hip_center_y, 'b-', linewidth=2, label='髋部高度 (Y坐标)')

# 标注起跳和落地
plt.axvline(takeoff_frame, color='r', linestyle='--', linewidth=2, label=f'起跳 (帧{takeoff_frame})')
plt.axvline(landing_frame, color='r', linestyle='--', linewidth=2, label=f'落地 (帧{landing_frame})')

# 标注最高点（髋部Y最大值）
max_idx = np.argmax(hip_center_y[takeoff_frame:landing_frame+1]) + takeoff_frame
max_y = hip_center_y[max_idx]
plt.plot(max_idx, max_y, 'go', markersize=10, label=f'最高点 (帧{max_idx})')

# 标签和标题（现在中文会完美显示，不会有方框）
plt.xlabel('帧号', fontsize=13)
plt.ylabel('Y 坐标 (像素)', fontsize=13)
plt.title('运动者1 立定跳远 - 重心高度变化曲线', fontsize=15, pad=15)

# 图例和网格优化
plt.legend(fontsize=11, loc='upper right')
plt.grid(True, alpha=0.3, linestyle='-')

# 自动调整布局，避免文字被截断
plt.tight_layout()

# ====================== 【优化：图片保存配置】 ======================
# 保存到当前代码所在文件夹，300dpi高分辨率，支持中文文件名
plt.savefig(
    '运动者1_重心高度变化曲线.png',  # 中文文件名，清晰好认
    dpi=300,          # 高分辨率，论文打印不模糊
    bbox_inches='tight',  # 自动裁剪多余空白
    facecolor='white' # 背景设为白色，避免透明底
)

# 显示图片
plt.show()

# ====================== 【新增：保存成功提示】 ======================
print("✅ 图片已成功生成！")
print("📁 文件名：运动者1_重心高度变化曲线.png")
print("📍 保存位置：当前代码所在的文件夹内")