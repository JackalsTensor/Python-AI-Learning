import numpy as np
import matplotlib.pyplot as plt
import os

# 设置保存路径（自动匹配你的文件夹结构）
save_dir = "D:\PythonProject1\深度学习\激活函数\激活函数图集"
os.makedirs(save_dir, exist_ok=True)

# 定义 ReLU 函数
def relu(x):
    return np.maximum(0, x)

# 生成数据
x = np.linspace(-10, 10, 100)
y = relu(x)

# 绘图
plt.figure(figsize=(8, 4))
plt.plot(x, y, color='red', linewidth=2, label='ReLU')
plt.axhline(y=0, color='gray', linestyle='--')
plt.axvline(x=0, color='gray', linestyle='--')

plt.title("ReLU 激活函数")
plt.xlabel("x")
plt.ylabel("ReLU(x)")
plt.legend()
plt.grid(True)

# 保存图片
save_path = os.path.join(save_dir, "relu_activation.png")
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"ReLU 图片已保存到：{save_path}")