import pandas as pd

long_df = pd.read_csv(r"D:\PythonProject1\数学建模\模拟2\资料\bike_long_table.csv")
print("所有列名：", long_df.columns.tolist())