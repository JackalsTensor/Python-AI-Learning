import numpy as np
import matplotlib.pyplot as plt
import os

# 保存路径
save_dir = "../激活函数图集"
os.makedirs(save_dir, exist_ok=True)

# 定义四个激活函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

def relu(x):
    return np.maximum(0, x)

def softmax(x):
    # Softmax 用于多输入，这里我们用它的导数/缩放形式在单轴上可视化趋势
    # 为了和其他函数在同一尺度对比，我们做一个简化的可视化
    exp_x = np.exp(x - np.max(x))
    return exp_x / np.sum(exp_x)

# 生成数据
x = np.linspace(-5, 5, 100)
y_sigmoid = sigmoid(x)
y_tanh = tanh(x)
y_relu = relu(x)

# 为了在同一张图上展示，Softmax 用一组离散点来表示
x_soft = np.linspace(-5, 5, 10)
y_soft = softmax(x_soft)

# 绘图
plt.figure(figsize=(10, 6))

plt.plot(x, y_sigmoid, label='Sigmoid', color='blue', linewidth=2)
plt.plot(x, y_tanh, label='Tanh', color='green', linewidth=2)
plt.plot(x, y_relu, label='ReLU', color='red', linewidth=2)
plt.scatter(x_soft, y_soft, label='Softmax (离散点)', color='orange', s=50, zorder=5)

# 辅助线
plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
plt.axvline(x=0, color='gray', linestyle=':', alpha=0.5)

plt.title('常见激活函数对比', fontsize=16)
plt.xlabel('输入 x', fontsize=12)
plt.ylabel('输出 y', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

# 保存图片
save_path = os.path.join(save_dir, "activation_functions_comparison.png")
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ 四个激活函数对比图已保存到：{save_path}")