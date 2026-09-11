import numpy as np
import matplotlib.pyplot as plt
import os

# 1. 设置保存路径
save_dir = "D:\PythonProject1\深度学习\激活函数\激活函数图集"
os.makedirs(save_dir, exist_ok=True)

# 2. sigmoid 函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# 3. 生成数据
x = np.linspace(-10, 10, 100)
y = sigmoid(x)

# 4. 绘图
plt.figure(figsize=(8, 4))
plt.plot(x, y, label='sigmoid(x)', color='blue', linewidth=2)
plt.axhline(y=0.5, color='red', linestyle='--', label='y=0.5')
plt.axvline(x=0, color='gray', linestyle=':')

plt.title('Sigmoid 函数曲线')
plt.xlabel('x')
plt.ylabel('sigmoid(x)')
plt.legend()
plt.grid(True)

# 5. 保存图片到指定文件夹
save_path = os.path.join(save_dir, "sigmoid_activation.png")
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Sigmoid 图片已保存到：{save_path}")