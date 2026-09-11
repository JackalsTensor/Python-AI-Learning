"""
案例:
    演示二分类任务的损失函数

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
细节:由于公式中没有包含Sigmoid损失函数，所以使用BCELoss的时候还需要手动指定Sigmoid
"""

#导包
import torch
import torch.nn as nn

#1.定义函数，演示二分类任务损失函数
def dm01():
    #1.设置真实值
    y_true=torch.tensor([0,1,0],dtype=torch.float)

    #2.设置预测值
    y_pred=torch.tensor([0.1,0.8,0.2],requires_grad= True,dtype=torch.float)

    #3.创建二分类交叉熵损失函数
    criterion=nn.BCELoss()

    #4.调用损失函数，计算损失
    loss=criterion(y_pred,y_true)
    print(f'损失值: {loss}')

#2.测试
if __name__ == '__main__':
    dm01()