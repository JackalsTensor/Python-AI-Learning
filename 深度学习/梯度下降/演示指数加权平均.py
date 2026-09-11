"""
案例:
   演示近30天，天气分布情况

"""

import torch
import numpy as np
import matplotlib.pyplot as plt

ELEMNT_NUMBER=30

#1.实际平均温度
def dm01():
    torch.manual_seed(0)
    #产生30天随机温度
    temperature=torch.randn(size=[ELEMNT_NUMBER])*10
    print(f'实际平均温度:{temperature}')
    #绘制平均温度
    days=torch.arange(1,ELEMNT_NUMBER+1,1)
    plt.plot(days,temperature,color='r')
    plt.scatter(days,temperature)
    plt.show()

#2.指数加权平均温度
def dm02(beta=0.9):
    torch.manual_seed(0)
    temperature=torch.randn(size=[ELEMNT_NUMBER])*10
    print(f'指数加权平均温度:{temperature}')

    exp_weight_avg = []
    for idx, temp in enumerate(temperature, 1):  # 修复：from → for
        if idx == 1:  # 修复：第一个元素直接加入
            exp_weight_avg.append(temp.item())
            continue
        # 计算 EMA
        prev = exp_weight_avg[-1]
        new_temp = beta * prev + (1 - beta) * temp.item()
        exp_weight_avg.append(new_temp)

    days = torch.arange(1, ELEMNT_NUMBER + 1, 1)
    plt.plot(days, exp_weight_avg, color='b', label='指数加权平均')
    plt.scatter(days, exp_weight_avg)
    plt.legend()
    plt.show()


# 运行
if __name__ == '__main__':
    # dm01()
    dm02(beta=0.5)
    dm02(beta=0.9)