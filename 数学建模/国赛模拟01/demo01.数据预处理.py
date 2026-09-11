#目标：将附件 2 的路段数据转化为建模可用的结构化数据，过滤禁行路段，计算核心参数。
import pandas as pd
#步骤 1.1：数据读取与格式校验
df = pd.read_csv(r"D:\PythonProject1\数学建模\国赛模拟01\roads_full.csv")
# print(df.head())
#步骤 1.2：单位标准化统一
#步骤 1.3：禁行路段筛选与标记
# 新增“是否禁行”列（1=禁行，0=有效）
df["是否禁行"] = df["初始积水深度(cm)"].apply(lambda x: 1 if x >=40 else 0)
# 拆分出禁行路段表和有效路段表
df_forbid = df[df["是否禁行"] == 1].copy()  # 禁行路段
df_valid = df[df["是否禁行"] == 0].copy()   # 有效路段
#步骤 1.4：有效路段速度匹配
def get_speed(h):
    if h < 20:
        return 40  # km/h
    elif 20 <= h < 40:
        return 20  # km/h
    else:
        return 0   # 禁行（已提前剔除，此处仅兜底）

# 为有效路段新增“通行速度(km/h)”列
df_valid["通行速度(km/h)"] = df_valid["初始积水深度(cm)"].apply(get_speed)
#步骤 1.5：计算路段通行时间
# 新增“通行时间(h)”列
df_valid["通行时间(h)"] = df_valid["长度(km)"] / df_valid["通行速度(km/h)"]
# 保留4位小数，避免精度冗余
df_valid["通行时间(h)"] = df_valid["通行时间(h)"].round(4)
#步骤 1.6：高风险路段标记与长度提取
# 新增“是否高风险”列（1=高风险，0=低风险）
df_valid["是否高风险"] = df_valid["初始积水深度(cm)"].apply(lambda x: 1 if 20<=x<40 else 0)
# 新增“高风险长度(km)”列：高风险路段取长度，低风险取0
df_valid["高风险长度(km)"] = df_valid.apply(lambda row: row["长度(km)"] if row["是否高风险"]==1 else 0, axis=1)
#步骤 1.7：过滤数据集信息
# 按积水深度和通行状态双重过滤
df_valid = df[(df["是否禁行"] == 0) & (df["通行状态"] == "可通行")].copy()
#步骤 1.8：补充特征列
def get_v(h):
    if h < 20:
        return 40
    else:
        return 20

df_valid["v"] = df_valid["初始积水深度(cm)"].apply(get_v)
df_valid["time"] = df_valid["长度(km)"] / df_valid["v"]
#步骤 1.9：数据保存
final_df = df_valid.rename(columns={
    "长度(km)": "length",
    "初始积水深度(cm)": "h"
})[["起点", "终点", "length", "h", "v", "time"]]

print(final_df.head())
final_df.to_csv("预处理后_路段表.csv", index=False, encoding="utf-8")