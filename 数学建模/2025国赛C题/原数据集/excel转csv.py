import pandas as pd


excel_file = "附件(1).xlsx"

#读取Excel文件里的两个工作表
df_male = pd.read_excel(excel_file, sheet_name="男胎检测数据")
df_female = pd.read_excel(excel_file, sheet_name="女胎检测数据")

df_male.to_csv("男胎检测数据.csv", index=False, encoding="utf-8-sig")
df_female.to_csv("女胎检测数据.csv", index=False, encoding="utf-8-sig")
