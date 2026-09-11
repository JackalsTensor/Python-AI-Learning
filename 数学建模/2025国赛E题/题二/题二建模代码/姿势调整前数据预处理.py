import pandas as pd
import numpy as np
import glob
import os

# ====================== 1. 配置路径（改成你自己的） ======================
# 你的姿势调整前Excel文件夹路径
excel_folder = r"D:\PythonProject1\数学建模\2025国赛E题\数据\姿势调整前"

# ====================== 2. 跳远成绩表（直接用你给的成绩，不用再读文件） ======================
score_dict = {
    "运动者3第1次": 1.33,
    "运动者3第2次": 1.40,
    "运动者3第3次": 1.32,
    "运动者3第4次": 1.36,
    "运动者3第5次": 1.39,
    "运动者4第1次": 1.80,
    "运动者5第1次": 2.05,
    "运动者5第2次": 2.05,
    "运动者6第1次": 1.15,
    "运动者6第2次": 1.15,
    "运动者7第1次": 1.82,
    "运动者7第2次": 1.90,
    "运动者8第1次": 1.45,
    "运动者8第2次": 1.47,
    "运动者9第1次": 1.45,
    "运动者10第1次": 1.50,
    "运动者10第2次": 1.52
}

# ====================== 3. 自动找所有Excel文件 ======================
file_list = glob.glob(os.path.join(excel_folder, "*.xlsx"))
file_list.sort()  # 按顺序排序

print(f"✅ 共找到 {len(file_list)} 个运动员数据文件")
for f in file_list:
    print(" -", os.path.basename(f))

# ====================== 4. 批量处理所有文件 ======================
all_data = []

for file_path in file_list:
    # 提取文件名中的运动员+次数
    file_name = os.path.basename(file_path).replace("的跳远位置信息.xlsx", "")
    print(f"\n正在处理：{file_name}")

    # 读取Excel
    df = pd.read_excel(file_path)

    # 提取关键点坐标
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

    # 固定起跳/落地帧（和你第一问一致）
    takeoff_frame = 16
    landing_frame = 244

    # 计算速度（中心差分法）
    vx = np.zeros(len(df))
    vy = np.zeros(len(df))
    for i in range(1, len(df)-1):
        vx[i] = (hip_center_x[i+1] - hip_center_x[i-1]) / 2
        vy[i] = (hip_center_y[i+1] - hip_center_y[i-1]) / 2

    # 提取核心指标
    takeoff_vx = vx[takeoff_frame]           # 起跳水平速度
    takeoff_vy = vy[takeoff_frame]           # 起跳垂直速度
    takeoff_speed = np.hypot(takeoff_vx, takeoff_vy)  # 起跳合速度
    takeoff_angle = angle[takeoff_frame]     # 起跳时刻身体倾角
    max_height = hip_center_y[takeoff_frame:landing_frame+1].max()  # 重心最大高度
    air_time = landing_frame - takeoff_frame # 滞空帧数
    jump_score = score_dict.get(file_name, np.nan)  # 匹配跳远成绩

    # 存入数据列表
    all_data.append({
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
df_total = pd.DataFrame(all_data)
df_total.to_excel("姿势调整前_全体运动员指标总表.xlsx", index=False)

print("\n🎉 全部处理完成！")
print("📁 已生成文件：姿势调整前_全体运动员指标总表.xlsx")
print("\n📊 数据预览：")
print(df_total)