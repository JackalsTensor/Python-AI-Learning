"""
案例:
    演示回归任务损失函数介绍
    回归问题:
            MAE:平均绝对误差
            MSE:均方误差
            Smooth L1:结合上述两个特点的升级，优化
"""
#导包
import torch
import torch.nn as nn

#1.定义函数，演示MAE损失函数
def dm01():
    #1.定义变量，记录真实值
    y_true=torch.tensor([1,2,3],dtype=torch.float)

    #2.定义变量，记录预测值
    y_pred=torch.tensor([1.5,2.5,2.5],requires_grad= True,dtype=torch.float)

    #3.创建MAE损失函数
    criterion=nn.L1Loss()

    #4.调用损失函数，计算损失
    loss=criterion(y_pred,y_true)
    print(f'损失值: {loss}')

#2.定义函数，演示MSE损失函数
def dm02():
    #1.定义变量，记录真实值
    y_true=torch.tensor([1,2,3],dtype=torch.float)

    #2.定义变量，记录预测值
    y_pred=torch.tensor([1.5,2.5,2.5],requires_grad= True,dtype=torch.float)

    #3.创建MSE损失函数
    criterion=nn.MSELoss()

    #4.调用损失函数，计算损失
    loss=criterion(y_pred,y_true)
    print(f'损失值: {loss}')

#3.定义函数，演示Smooth L1损失函数
def dm03():
    #1.定义变量，记录真实值
    y_true=torch.tensor([1,2,3],dtype=torch.float)

    #2.定义变量，记录预测值
    y_pred=torch.tensor([1.5,2.5,2.5],requires_grad= True,dtype=torch.float)

    #3.创建Smooth L1损失函数
    criterion=nn.SmoothL1Loss()

    #4.调用损失函数，计算损失
    loss=criterion(y_pred,y_true)
    print(f'损失值: {loss}')


#4.测试
if __name__ == '__main__':
    dm01()
    dm02()
    dm03()