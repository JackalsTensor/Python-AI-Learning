#导包
import torch

#1.定义变量,记录:初始的权重w(旧)
w=torch.tensor(10,requires_grad=True,dtype=torch.float)

#2.定义loss变量,表示损失函数
loss=2*w**2

#3.打印梯度函数类型
# print(f'初始的loss是：{loss}')
# print(f'梯度函数类型:{type(loss.grad_fn)}')
# print(loss.sum())

#4.计算梯度,梯度=损失函数导数
loss.backward()

#5.带入权重更新公式:w新=w旧-学习率*梯度
w.data=w.data-0.01*w.grad.data

#6.打印最终结果
print(f'更新后的w是：{w}')
print(f'更新后的loss是：{loss}')
print(f'梯度函数类型:{type(loss.grad_fn)}')

#7.结果展示
"""
更新后的w是：9.600000381469727
更新后的loss是：200.0
梯度函数类型:<class 'MulBackward0'>
"""