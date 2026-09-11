"""
案例:
    演示参数初始化的 7 种方式.

参数初始化的目的:
    1. 防止梯度消失 或者 梯度爆炸.
    2. 提高收敛速度.
    3. 打破对称性.

参数初始化的方式:
    无法打破对称性的:
        全0, 全1, 固定值
    可以打破对称性的:
        随机初始化, 正态分布初始化, kaiming初始化, xavier初始化

总结:
    1. 记忆 kaiming初始化, xavier初始化, 全0初始化.
    2. 关于初始化的选择上:
        激活函数ReLU及其系列: 优先用 kaiming
        激活函数非ReLU: 优先用 xavier
        如果是浅层网络: 可以考虑使用 随机初始化
"""
#导包
import torch.nn as nn
#1.均匀分布初始化
def dm01():
    #1.创建一个线性层
    linear=nn.Linear(in_features=5,out_features=3)
    #2.对权重(w)进行随机初始化,从0到1的均匀分布中随机取值
    nn.init.uniform_(linear.weight)
    #3.对偏置(b)进行随机初始化,从0到1的均匀分布中随机取值
    nn.init.uniform_(linear.bias)
    #4.打印生成结果
    print(linear.weight)
    print(linear.bias)

#2.固定初始化
def dm02():
    #1.创建一个线性层,输入维度5,输出维度3
    linear=nn.Linear(5,3)
    #2.对权重(w)进行随机初始化,从0到1的均匀分布中产生参数
    nn.init.constant_(linear.weight,0)
    #3.对偏置(b)进行随机初始化,从0到1的均匀分布中产生参数
    nn.init.constant_(linear.bias,0)
    #4.打印生成结果
    print(linear.weight.data)
    print(linear.bias.data)

# 3. 全0初始化
def dm03():
    # 1. 创建1个线性层, 输入维度5, 输出维度3
    linear = nn.Linear(in_features=5, out_features=3)
    # 2. 对权重(w)进行随机初始化, 从0-1均匀分布产生参数
    nn.init.zeros_(linear.weight)
    # 3. 对偏置(b)进行随机初始化, 从0-1均匀分布产生参数
    nn.init.zeros_(linear.bias)
    # 4. 打印生成结果.
    print(linear.weight.data)
    print(linear.bias.data)

#4.全1初始化
def dm04():
    #1.创建一个线性层,输入维度5,输出维度3
    linear=nn.Linear(5,3)
    #2.对权重(w)进行随机初始化,从0到1的均匀分布中产生参数
    nn.init.ones_(linear.weight)
    #3.对偏置(b)进行随机初始化,从0到1的均匀分布中产生参数
    nn.init.ones_(linear.bias)
    #4.打印生成结果
    print(linear.weight.data)
    print(linear.bias.data)

#5.正态分布初始化
def dm05():
    #1.创建一个线性层,输入维度5,输出维度3
    linear=nn.Linear(5,3)
    #2.对权重(w)进行随机初始化,从0到1的均匀分布中产生参数
    nn.init.normal_(linear.weight,mean=0,std=1)
    #3.对偏置(b)进行随机初始化,从0到1的均匀分布中产生参数
    nn.init.normal_(linear.bias,mean=0,std=1)
    #4.打印生成结果
    print(linear.weight.data)
    print(linear.bias.data)

#6.kaiming初始化
def dm06():
    #1.创建一个线性层,输入维度5,输出维度3
    linear=nn.Linear(5,3)
    #2.对权重(w)进行随机初始化,从0到1的均匀分布中产生参数
    nn.init.kaiming_normal_(linear.weight,mode='fan_in',nonlinearity='relu')
    #3.打印生成结果
    print(linear.weight.data)

#7.xavier初始化
def dm07():
    #1.创建一个线性层,输入维度5,输出维度3
    linear=nn.Linear(5,3)
    #2.对权重(w)进行随机初始化,从0到1的均匀分布中产生参数
    nn.init.xavier_normal_(linear.weight)
    #3.打印生成结果
    print(linear.weight.data)

#测试
if __name__ == '__main__':
    dm01()  #均匀分布初始化
    dm02()   #固定初始化
    dm03()   #全0初始化
    dm04()   #全1初始化
    dm05()   #正态分布初始化
    dm06()   #kaiming初始化
    dm07()    #xavier初始化

#运行结果
"""
Parameter containing:
tensor([[0.0324, 0.4575, 0.0178, 0.6686, 0.0919],
        [0.4729, 0.0537, 0.6984, 0.8452, 0.3849],
        [0.7827, 0.9645, 0.4513, 0.4974, 0.1753]], requires_grad=True)
Parameter containing:
tensor([0.1305, 0.0706, 0.7119], requires_grad=True)
tensor([[0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0.]])
tensor([0., 0., 0.])
tensor([[0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0.],
        [0., 0., 0., 0., 0.]])
tensor([0., 0., 0.])
tensor([[1., 1., 1., 1., 1.],
        [1., 1., 1., 1., 1.],
        [1., 1., 1., 1., 1.]])
tensor([1., 1., 1.])
tensor([[ 0.2515,  0.5347, -0.0155,  0.2199,  0.7949],
        [ 0.4405, -1.2648,  1.3063,  0.1555, -0.6698],
        [ 0.3522,  1.1013,  2.3354, -0.1833,  0.5367]])
tensor([ 0.5139, -0.7874, -0.1113])
tensor([[ 0.2277,  0.0525,  0.0446, -0.5168,  0.6570],
        [ 0.2133, -0.1721,  0.5316,  0.5348, -0.3194],
        [-0.8645, -0.7742,  0.2317, -0.1508, -0.7729]])
tensor([[ 1.2222,  0.0029, -0.6214,  0.3316,  0.1064],
        [-0.5182, -0.3484, -0.7990, -0.2357, -1.1501],
        [-0.3653, -0.0913, -0.3119,  0.4409,  0.6322]])
"""