"""
梯度下降相关介绍:

概述:
梯度下降是结合 本次损失函数的导数(作为梯度) 基于学习率 来更新权重的.

公式:
W新 = W旧 - 学习率 * (本次的)梯度

存在的问题:
1. 遇到平缓区域, 梯度下降(权重更新)可能会慢.
2. 可能会遇到 鞍点(梯度为0)
3. 可能会遇到 局部最小值.

解决思路:
从上述的 学习率 或者 梯度入手, 进行优化, 于是有了: 动量法Momentum, 自适应学习率AdaGrad, RMSProp, 综合衡量: Adam


动量法Momentum:

动量法公式:
St = β * St-1 + (1 - β) * Gt

解释:
St:     本次的指数移动加权平均结果.
β:      调节权重系数, 越大, 数据越平缓, 历史指数移动加权平均 比重越大, 本次梯度权重越小.
St-1:   历史的指数移动加权平均结果.
Gt:     本次计算出的梯度(不考虑历史梯度).

加入动量法后的 梯度更新公式:
W新 = W旧 - 学习率 * St
"""

import torch
import torch.nn as nn

from 机器学习.聚类.聚类算法演示 import criterion


#1.定义函数，演示梯度下降优化方法 -->  动量法(Momentum)
def dm01_moentum():
    #1.1.初始化权重函数
    w = torch.tensor([1.0], requires_grad=True, dtype=torch.float32)
    #1.2.定义损失函数
    criterion=((w**2)/2.0)
    #1.3.创建优化器(函数对象) --> 基于SGD(随机梯度下降)，加入参数 momentum，就是动量法
    optimizer=torch.optim.SGD(params=[w],lr=0.01,momentum=0.9)
    #1.4.计算梯度值:
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w: {w}, 梯度值: {w.grad}')
    #1.5.重复上述步骤，重新计算梯度值
    criterion=((w**2)/2.0)
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w: {w}, 梯度值: {w.grad}')

#2.定义函数，演示梯度下降优化方法 -->  自适应学习率(AdaGrad)
def dm02_AdaGrad():
    # 2.1.初始化权重函数
    w = torch.tensor([1.0], requires_grad=True, dtype=torch.float32)
    # 2.2.定义损失函数
    criterion = ((w ** 2) / 2.0)
    # 2.3.创建优化器(函数对象) --> 基于SGD(随机梯度下降)，加入参数 momentum，就是动量法
    optimizer = torch.optim.Adagrad(params=[w], lr=0.01)
    # 2.4.计算梯度值:
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w: {w}, 梯度值: {w.grad}')
    # 2.5.重复上述步骤，重新计算梯度值
    criterion = ((w ** 2) / 2.0)
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w: {w}, 梯度值: {w.grad}')

#3.定义函数，演示梯度下降优化方法 -->  RMSProp
def dm03_RMSProp():
    # 3.1.初始化权重函数
    w = torch.tensor([1.0], requires_grad=True, dtype=torch.float32)
    # 3.2.定义损失函数
    criterion = ((w ** 2) / 2.0)
    # 3.3.创建优化器(函数对象) --> 基于SGD(随机梯度下降）
    optimizer = torch.optim.RMSprop(params=[w], lr=0.01)
    # 3.4.计算梯度值:
    optimizer.zero_grad()
    criterion.sum().backward()
    optimizer.step()
    print(f'w: {w}, 梯度值: {w.grad}')







#5.测试
if __name__ == '__main__':
    #dm01_moentum()
    #dm02_AdaGrad()
    dm03_RMSProp()

