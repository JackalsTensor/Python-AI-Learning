import numpy as np
import matplotlib.pyplot as plt
import os

# 1. 定义保存路径（确保文件夹存在）
save_dir = "D:\PythonProject1\深度学习\激活函数\激活函数图集"
os.makedirs(save_dir, exist_ok=True)

# 2. 定义 Tanh 函数
def tanh(x):
    return np.tanh(x)

# 3. 生成数据
x = np.linspace(-10, 10, 100)
y = tanh(x)

# 4. 绘图
plt.figure(figsize=(8, 4))
plt.plot(x, y, color='green', linewidth=2, label='tanh(x)')
plt.axhline(y=0, color='red', linestyle='--')  # 中心线
plt.axvline(x=0, color='gray', linestyle=':')

plt.title("Tanh 激活函数")
plt.xlabel("x")
plt.ylabel("tanh(x)")
plt.legend()
plt.grid(True)

# 5. 保存图片到指定文件夹
save_path = os.path.join(save_dir, "tanh_activation.png")
plt.savefig(save_path, dpi=300, bbox_inches='tight')  # dpi=300保证清晰度，bbox避免标题被截断
plt.close()

print(f"图片已保存到：{save_path}")