import pandas as pd
import numpy as np
import glob
import os

# ====================== 1. 配置路径（改成你自己的） ======================
# 你的姿势调整后Excel文件夹路径
excel_folder = r"D:\PythonProject1\数学建模\2025国赛E题\数据\姿势调整后"

# ====================== 2. 调整后跳远成绩表（直接用你给的成绩） ======================
score_dict_after = {
    "运动者3调整后第1次": 1.58,
    "运动者3调整后第2次": 1.40,
    "运动者4调整后第1次": 1.95,
    "运动者4调整后第2次": 1.97,
    "运动者5调整后第1次": 2.15,
    "运动者5调整后第2次": 2.16,
    "运动者6调整后第1次": 1.28,
    "运动者6调整后第2次": 1.35,
    "运动者7调整后第1次": 2.05,
    "运动者7调整后第2次": 2.05,
    "运动者8调整后第1次": 1.50,
    "运动者9调整后第1次": 1.53,
    "运动者9调整后第2次": 1.45,
    "运动者10调整后第1次": 1.62,
    "运动者10调整后第2次": 1.60
}

# ====================== 3. 自动找所有Excel文件 ======================
file_list = glob.glob(os.path.join(excel_folder, "*.xlsx"))
file_list.sort()  # 按顺序排序

print(f"✅ 共找到 {len(file_list)} 个调整后运动员数据文件")
for f in file_list:
    print(" -", os.path.basename(f))

# ====================== 4. 批量处理所有文件 ======================
all_data_after = []

for file_path in file_list:
    # 提取文件名中的运动员+次数
    file_name = os.path.basename(file_path).replace("的跳远位置信息.xlsx", "")
    print(f"\n正在处理：{file_name}")

    # 读取Excel
    df = pd.read_excel(file_path)

    # 提取关键点坐标（和调整前完全一致，保证指标可比）
    left_hip_x = df['21_X']
    left_hip_y = df['21_Y']
    right_hip_x = df['22_X']
    right_hip_y = df['22_Y']
    left_shoulder_x = df['5_X']
    left_shoulder_y = df['5_Y']
    right_shoulder_x = df['6_X']
    right_shoulder_y = df['6_Y']

    # 计算重心（髋部中点）
    hip_center_x = (left_hip_x + right_hip_x) / 2
    hip_center_y = (left_hip_y + right_hip_y) / 2

    # 计算身体倾角
    dx = (left_shoulder_x + right_shoulder_x)/2 - hip_center_x
    dy = (left_shoulder_y + right_shoulder_y)/2 - hip_center_y
    angle = np.arctan2(dy, dx) * 180 / np.pi

    # 固定起跳/落地帧（和你第一问、调整前完全一致）
    takeoff_frame = 16
    landing_frame = 244

    # 计算速度（中心差分法，和调整前算法统一）
    vx = np.zeros(len(df))
    vy = np.zeros(len(df))
    for i in range(1, len(df)-1):
        vx[i] = (hip_center_x[i+1] - hip_center_x[i-1]) / 2
        vy[i] = (hip_center_y[i+1] - hip_center_y[i-1]) / 2

    # 提取核心指标（和调整前完全统一，保证前后可对比）
    takeoff_vx = vx[takeoff_frame]           # 起跳水平速度
    takeoff_vy = vy[takeoff_frame]           # 起跳垂直速度
    takeoff_speed = np.hypot(takeoff_vx, takeoff_vy)  # 起跳合速度
    takeoff_angle = angle[takeoff_frame]     # 起跳时刻身体倾角
    max_height = hip_center_y[takeoff_frame:landing_frame+1].max()  # 重心最大高度
    air_time = landing_frame - takeoff_frame # 滞空帧数
    jump_score = score_dict_after.get(file_name, np.nan)  # 匹配跳远成绩

    # 存入数据列表
    all_data_after.append({
        "运动员测试": file_name,
        "跳远成绩(米)": jump_score,
        "起跳水平速度vx": round(takeoff_vx, 2),
        "起跳垂直速度vy": round(takeoff_vy, 2),
        "起跳合速度": round(takeoff_speed, 2),
        "起跳时刻倾角(°)": round(takeoff_angle, 2),
        "重心最大高度": round(max_height, 2),
        "滞空帧数": air_time
    })

# ====================== 5. 导出总表 ======================
df_total_after = pd.DataFrame(all_data_after)
df_total_after.to_excel("姿势调整后_全体运动员指标总表.xlsx", index=False)

print("\n🎉 姿势调整后数据全部处理完成！")
print("📁 已生成文件：姿势调整后_全体运动员指标总表.xlsx")
print("\n📊 数据预览：")
print(df_total_after)