"""
案例:
    演示多分类任务交叉熵损失函数

损失函数介绍
    概述:
        损失函数又叫成本函数，目标函数，代价函数，误差函数，就是用来衡量模型好坏(模型拟合情况)的
    分类:
        分类问题:
            多分类交叉损失:CrossEntropyLoss
            二分类交叉熵损失:BCELoss
        回归问题:
            MAE:平均绝对误差
            MSE:均方误差
            Smooth L1:结合上述两个特点的升级，优化

"""
#导包
import torch
import torch.nn as nn

#1.定义函数，演示多分类交叉熵损失
def dm01():
    #1.手动创建样本的真实值 -> 就是上述分式中的y
    #y_true=torch.tensor([[0,1,0],[0,0,1]],dtype=torch.float)
    y_true=torch.tensor([1,2])

    #2.手动创建样本的预测值 -> 就是上述分式中的f(x)
    y_pred=torch.tensor([[0.1,0.9,0.2],[0.7,0.1,0.2]],requires_grad= True,dtype=torch.float)

    #3.创建多分类交叉熵损失函数
    criterion=nn.CrossEntropyLoss()

    #4.调用损失函数，计算损失
    loss=criterion(y_pred,y_true)
    print(f'损失值: {loss}')
#2.测试
if __name__ == '__main__':
    dm01()