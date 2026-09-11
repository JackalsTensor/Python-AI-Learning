# 导入PyTorch核心库
import torch
import torch.nn as nn
import torch.optim as optim

# ====================== 第一步：验证PyTorch环境 ======================
print("===== 环境验证 =====")
# 打印PyTorch版本
print(f"PyTorch版本: {torch.__version__}")
# 验证CPU是否可用（CPU版这里一定是True）
print(f"CPU是否可用: {torch.cpu.is_available()}")
# 生成一个简单的张量（PyTorch核心数据结构）
x = torch.randn(5, 3)  # 5行3列的随机数张量
print(f"随机张量示例:\n{x}\n")

# ====================== 第二步：简单神经网络训练 ======================
print("===== 简单神经网络训练 =====")


# 1. 定义一个超简单的线性回归模型（本科入门最常用）
class SimpleLinearModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 线性层：1个输入特征 → 1个输出特征
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        # 前向传播（模型的核心计算逻辑）
        return self.linear(x)


# 2. 准备训练数据（模拟y = 2x + 1的线性关系，加一点噪声）
# 生成100个训练样本，CPU版无需指定device，自动用CPU
x_train = torch.randn(100, 1)  # 输入：100个样本，每个样本1个特征
y_train = 2 * x_train + 1 + 0.1 * torch.randn(100, 1)  # 输出：带噪声的线性结果

# 3. 初始化模型、损失函数、优化器
model = SimpleLinearModel()  # 创建模型实例
criterion = nn.MSELoss()  # 均方误差损失（回归任务常用）
optimizer = optim.SGD(model.parameters(), lr=0.01)  # 随机梯度下降优化器

# 4. 训练模型（跑100轮）
epochs = 100
for epoch in range(epochs):
    # 清零梯度（PyTorch必须步骤）
    optimizer.zero_grad()
    # 前向传播：用模型预测
    y_pred = model(x_train)
    # 计算损失
    loss = criterion(y_pred, y_train)
    # 反向传播：计算梯度
    loss.backward()
    # 更新模型参数
    optimizer.step()

    # 每10轮打印一次损失（看训练是否收敛）
    if (epoch + 1) % 10 == 0:
        print(f"第 {epoch + 1} 轮训练，损失值: {loss.item():.4f}")

# ====================== 第三步：测试模型效果 ======================
print("\n===== 模型测试 =====")
# 用训练好的模型预测新数据
x_test = torch.tensor([[2.0]])  # 测试输入：x=2
y_test = model(x_test)  # 模型预测
print(f"输入x=2时，模型预测值: {y_test.item():.4f}")
print(f"真实值（y=2*2+1=5）: 5.0000")

# 打印模型训练后的参数（理想值：权重≈2，偏置≈1）
for name, param in model.named_parameters():
    print(f"{name}: {param.item():.4f}")

print("\n✅ 测试完成！PyTorch CPU版运行正常！")