""""
演示神经网络搭建流程

深度学习案例的4个步骤：
    1.准备数据
    2.搭建神经网络
    3.模型训练
    4.模型测试

神经网络搭建流程：
    1.定义一个类，继承：nn.Module
    2.在__init__()方法中，搭建神经网络
    3.在forward()方法中,完成:前向传播
"""

#导包
import torch
import torch.nn as nn  # 神经网络核心模块：层、激活函数、损失函数
from torchsummary import summary #计算模型参数，查看模型结构

#todo: 1.搭建神经网络，即:自定义继承 nn.Module
class ModelDemo(nn.Module):
    #todo 1.1 在init魔法方法中，完成初始化:父类成员,及神经网络搭建
    def __init__(self):
        #1.1 父类成员初始化
        super().__init__()
        #1.2 搭建神经网络->隐藏层 + 输出层
        #隐藏层1:输入特指数 3，输出特征数 3
        self.linear1=nn.Linear(in_features=3,out_features=3)
        #隐藏层2:输入特征数 3，输出特征数 2
        self.linear2=nn.Linear(in_features=3,out_features=2)
        #输出层:输入特征数 2，输出特征数 2
        self.linear3=nn.Linear(in_features=2,out_features=2)
        #1.3 对隐藏层进行参数初始化
        # 隐藏层1：weight用xavier正态分布，bias置0
        nn.init.xavier_normal_(self.linear1.weight)
        nn.init.zeros_(self.linear1.bias)
        # 隐藏层2：weight用kaiming正态分布，bias置0
        nn.init.kaiming_normal_(self.linear2.weight)
        nn.init.zeros_(self.linear2.bias)
    #todo 1.2 前向传播:输入数据 -> 隐藏层 -> 输出层
    def forward(self,x):
        #1.1 第一层：线性变换 + sigmoid激活
        # x=self.linear1(x)
        # x=torch.sigmoid(x)
        x=torch.sigmoid(self.linear1(x))
        #1.2 第二层：线性变换 + relu激活
        x=torch.relu(self.linear2(x))
        #1.3 输出层：线性变换 + softmax激活(最后一维归一化)
        x=torch.softmax(self.linear3(x),dim=-1)   #dim=-1表示对最后一维（特征维）求和为 1
        #1.4 返回预测值
        return x

#todo: 2.模型预测
def train():
    #1.创建模型对象
    my_model=ModelDemo()
    # print(my_model)

    #2.生成随机测试数据：形状[5,3]
    data=torch.randn(size=(5,3))
    print(f'data: {data}')# 打印数据值
    print(f'data.shape: {data.shape}')# 打印维度：torch.Size([5, 3])
    print(f'data.requires_grad: {data.requires_grad}')# 默认为False

    #3.调用神经网络模型，进行模型训练
    output=my_model(data)    #自动调用了forward()方法进行前向传播
    print(f'output: {output}') # 打印预测结果（5个样本，每个样本2个概率值
    print(f'output.shape: {output.shape}') # torch.Size([5, 2])
    print(f'output.requires_grad: {output.requires_grad}')  # True

    #4.可视化网络结构+参数统计
    summary(my_model,input_size=(5,3))   # input_size：(样本数, 特征数)

    # 5. 遍历打印所有参数（name=参数名，param=参数值
    for name,param in my_model.named_parameters():
        print(f'name: {name}')
        print(f'param: {param}')
        print(f'param.shape: {param.shape}')
        print(f'param.requires_grad: {param.requires_grad}')
        print('-'*50)
#todo: 3.测试
if __name__ == '__main__':
    train()

#todo: 4.结果展示
"""
data: tensor([[ 0.7556,  0.1976,  0.5601],
        [ 1.9580, -0.2064,  0.5149],
        [ 1.3270, -0.7005,  1.6685],
        [-0.4201, -1.4239,  0.5233],
        [-0.6029,  1.6450, -0.6932]])
data.shape: torch.Size([5, 3])
data.requires_grad: False
output: tensor([[0.3935, 0.6065],
        [0.3818, 0.6182],
        [0.3701, 0.6299],
        [0.3524, 0.6476],
        [0.4356, 0.5644]], grad_fn=<SoftmaxBackward0>)
output.shape: torch.Size([5, 2])
output.requires_grad: True
----------------------------------------------------------------
        Layer (type)               Output Shape         Param #
================================================================
            Linear-1                 [-1, 5, 3]              12
            Linear-2                 [-1, 5, 2]               8
            Linear-3                 [-1, 5, 2]               6
================================================================
Total params: 26
Trainable params: 26
Non-trainable params: 0
----------------------------------------------------------------
Input size (MB): 0.00
Forward/backward pass size (MB): 0.00
Params size (MB): 0.00
Estimated Total Size (MB): 0.00
----------------------------------------------------------------
name: linear1.weight
param: Parameter containing:
tensor([[-0.3386,  0.6537, -0.8134],
        [-1.0646, -0.0405, -0.2615],
        [-0.1294,  0.8641,  0.6210]], requires_grad=True)
param.shape: torch.Size([3, 3])
param.requires_grad: True
--------------------------------------------------
name: linear1.bias
param: Parameter containing:
tensor([0., 0., 0.], requires_grad=True)
param.shape: torch.Size([3])
param.requires_grad: True
--------------------------------------------------
name: linear2.weight
param: Parameter containing:
tensor([[ 0.6102, -0.0555, -0.6289],
        [ 0.9177, -0.3906,  0.3968]], requires_grad=True)
param.shape: torch.Size([2, 3])
param.requires_grad: True
--------------------------------------------------
name: linear2.bias
param: Parameter containing:
tensor([0., 0.], requires_grad=True)
param.shape: torch.Size([2])
param.requires_grad: True
--------------------------------------------------
name: linear3.weight
param: Parameter containing:
tensor([[ 0.6182, -0.1913],
        [ 0.7047, -0.6768]], requires_grad=True)
param.shape: torch.Size([2, 2])
param.requires_grad: True
--------------------------------------------------
name: linear3.bias
param: Parameter containing:
tensor([-0.3842,  0.2720], requires_grad=True)
param.shape: torch.Size([2])
param.requires_grad: True
--------------------------------------------------
"""