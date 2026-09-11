import numpy as np
import matplotlib.pyplot as plt
import os

# 保存路径
save_dir = "../激活函数图集"
os.makedirs(save_dir, exist_ok=True)

# 定义 Softmax 函数
def softmax(x):
    exp_x = np.exp(x - np.max(x))  # 减去最大值防止溢出
    return exp_x / np.sum(exp_x)

# 生成一组测试数据
x = np.array([1, 2, 3, 4, 5])
y = softmax(x)

# 绘图（柱状图最适合展示 Softmax）
plt.figure(figsize=(8, 4))
plt.bar(x, y, color='orange', label='Softmax')
plt.title("Softmax 激活函数")
plt.xlabel("输入值")
plt.ylabel("概率值")
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
save_path = os.path.join(save_dir, "softmax_activation.png")
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Softmax 图片已保存到：{save_path}")