import kagglehub
import os
import shutil
# 下载数据集（会自动下载到 kagglehub 的缓存目录）
path = kagglehub.dataset_download("hasibalmuzdadid/global-air-pollution-dataset")
print("数据集下载到临时目录:", path)
# 你的目标文件夹
target_dir = r"D:\PythonProject1\数据集\全球城市空气质量数据集"

# 如果目标文件夹不存在，就创建
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# 把下载好的所有文件移动到目标文件夹
for file_name in os.listdir(path):
    src = os.path.join(path, file_name)
    dst = os.path.join(target_dir, file_name)
    shutil.move(src, dst)

print("数据集已成功移动到:", target_dir)