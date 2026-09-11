import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 读取原始数据
df = pd.read_csv(r"D:\PythonProject1\核心项目库\基于 CBDB 的中国古代士人仕途与科举预测研究\cbdb_biog_main.csv")

# 2. 先删除无价值特征（注意：这里要赋值回 df，或者用新变量）
df = df.drop(columns=[
    "c_tribe",  # 全为空特征
    "c_created_by", "c_modified_by", "c_created_date", "c_modified_date",  # 与历史研究无关
    "c_surname_rm", "c_mingzi_rm", "c_name_rm",  # 空值太多
    "c_dy_day_gz", "c_surname_proper", "c_mingzi_proper", "c_name_proper",
    "c_dy_month", "c_by_month", "c_by_day", "c_dy_day", "c_by_day_gz", "c_dy_day_gz",
    "c_by_intercalary", "c_dy_intercalary",
    "c_name", "c_name_chn", "c_surname", "c_mingzi", "c_mingzi_chn",
    "c_fl_ey_notes", "c_fl_ly_notes", "c_notes",
    "c_by_nh_year", "c_dy_nh_year", "c_fl_ey_nh_year", "c_fl_ly_nh_year",
    "c_by_range", "c_dy_range", "c_death_age_range",
    # 新增的强相关冗余特征（从左边复制过来）
    "c_by_nh_code", "c_dy_nh_code", "c_fl_ey_nh_code", "c_fl_ly_nh_code", "c_deathyear"
])

# 3. 再删除核心字段缺失的样本
core_fields = ["c_personid", "c_female", "c_birthyear", "c_index_year", "c_surname_chn"]
df.dropna(subset=core_fields)

# 4. 保存清洗后的数据
df.to_csv("cbdb_final_data.csv", index=False)

# 5. 验证：读取并查看清洗后的数据
df_check = pd.read_csv("cbdb_final_data.csv")
# print("清洗后数据形状：", df_check.shape)
# print(df_check.info())

# 6. 绘制相关性热力图
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


# 筛选数值特征
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
# 计算相关性矩阵
corr = df[numeric_cols].corr()

# 绘制相关性热力图
plt.figure(figsize=(12, 10))
sns.heatmap(
    corr,
    annot=False,
    cmap="coolwarm",
    vmin=-1, vmax=1,
    linewidths=0.5
)
plt.title("CBDB数据集数值特征相关性热力图", fontsize=14)
plt.tight_layout()
plt.savefig("corr_heatmap.png", dpi=300)
# plt.show()
#根据特征热力图发现，大部分特征之间无强相关，特征冗余度低，适合建模
drop_features = [
    "c_by_nh_code",    # 和c_birthyear强相关，保留c_birthyear（公元年份更直观）
    "c_dy_nh_code",    # 和c_deathyear强相关，保留c_deathyear
    "c_fl_ey_nh_code", # 和c_fl_earliest_year强相关，保留c_fl_earliest_year
    "c_fl_ly_nh_code", # 和c_fl_latest_year强相关，保留c_fl_latest_year
    "c_deathyear"      # 和c_death_age强相关，保留c_death_age（年龄更有业务意义）
]