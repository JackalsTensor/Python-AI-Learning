"""
演示神经网络搭建流程 + 神经元可视化（修复中文乱码+自动保存到文件夹）
深度学习案例的4个步骤：
    1.准备数据
    2.搭建神经网络
    3.模型训练
    4.模型测试 + 可视化
"""
# 基础库
import torch
import torch.nn as nn
from torchsummary import summary
# 可视化库
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import numpy as np
# 新增：用于创建文件夹
import os

# ===================== 关键修复：解决中文乱码问题 =====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 新增：创建保存图片的文件夹（不存在则自动创建）
SAVE_DIR = 'network_visualization_results'
os.makedirs(SAVE_DIR, exist_ok=True)

# ===================== 1. 搭建神经网络（原有逻辑保留） =====================
class ModelDemo(nn.Module):
    def __init__(self):
        super().__init__()
        # 隐藏层1:输入3维 → 输出3维
        self.linear1 = nn.Linear(in_features=3, out_features=3)
        # 隐藏层2:输入3维 → 输出2维
        self.linear2 = nn.Linear(in_features=3, out_features=2)
        # 输出层:输入2维 → 输出2维
        self.linear3 = nn.Linear(in_features=2, out_features=2)

        # 参数初始化（原有逻辑）
        nn.init.xavier_normal_(self.linear1.weight)
        nn.init.zeros_(self.linear1.bias)
        nn.init.kaiming_normal_(self.linear2.weight)
        nn.init.zeros_(self.linear2.bias)

    def forward(self, x):
        # 保存每层输出（用于可视化神经元激活值）
        self.layer1_out = torch.sigmoid(self.linear1(x))  # 隐藏层1输出
        self.layer2_out = torch.relu(self.linear2(self.layer1_out))  # 隐藏层2输出
        self.layer3_out = torch.softmax(self.linear3(self.layer2_out), dim=-1)  # 输出层
        return self.layer3_out

# ===================== 2. 新增：神经元可视化函数 =====================
def visualize_neurons(model, data, save_dir):
    """
    可视化神经元核心信息：
    1. 每层权重分布（直方图）
    2. 每层神经元激活值（热力图）
    3. 网络拓扑结构（节点=神经元，边=权重）
    """
    # 先执行前向传播，获取每层输出
    _ = model(data)

    # ---------- 子图1：每层权重分布直方图 ----------
    plt.figure(figsize=(15, 10))

    # 隐藏层1权重
    plt.subplot(2, 3, 1)
    weights = model.linear1.weight.detach().numpy().flatten()
    plt.hist(weights, bins=10, color='skyblue', edgecolor='black')
    plt.title('隐藏层1 权重分布')
    plt.xlabel('权重值')
    plt.ylabel('频次')

    # 隐藏层2权重
    plt.subplot(2, 3, 2)
    weights = model.linear2.weight.detach().numpy().flatten()
    plt.hist(weights, bins=10, color='lightgreen', edgecolor='black')
    plt.title('隐藏层2 权重分布')
    plt.xlabel('权重值')
    plt.ylabel('频次')

    # 输出层权重
    plt.subplot(2, 3, 3)
    weights = model.linear3.weight.detach().numpy().flatten()
    plt.hist(weights, bins=10, color='salmon', edgecolor='black')
    plt.title('输出层 权重分布')
    plt.xlabel('权重值')
    plt.ylabel('频次')

    # ---------- 子图2：每层神经元激活值（热力图） ----------
    # 隐藏层1激活值（5个样本×3个神经元）
    plt.subplot(2, 3, 4)
    layer1_act = model.layer1_out.detach().numpy()
    sns.heatmap(layer1_act, cmap='Blues', annot=True, fmt='.2f')
    plt.title('隐藏层1 神经元激活值（sigmoid）')
    plt.xlabel('神经元编号')
    plt.ylabel('样本编号')

    # 隐藏层2激活值（5个样本×2个神经元）
    plt.subplot(2, 3, 5)
    layer2_act = model.layer2_out.detach().numpy()
    sns.heatmap(layer2_act, cmap='Greens', annot=True, fmt='.2f')
    plt.title('隐藏层2 神经元激活值（ReLU）')
    plt.xlabel('神经元编号')
    plt.ylabel('样本编号')

    # 输出层激活值（5个样本×2个神经元）
    plt.subplot(2, 3, 6)
    layer3_act = model.layer3_out.detach().numpy()
    sns.heatmap(layer3_act, cmap='Reds', annot=True, fmt='.2f')
    plt.title('输出层 神经元激活值（Softmax）')
    plt.xlabel('神经元编号')
    plt.ylabel('样本编号')

    plt.tight_layout()
    # 保存到指定文件夹
    save_path1 = os.path.join(save_dir, '神经元激活值与权重分布.png')
    plt.savefig(save_path1, dpi=150, bbox_inches='tight')
    plt.close()  # 关闭当前画布，避免影响下一张图
    print(f"已保存：{save_path1}")

    # ---------- 单独可视化：网络拓扑结构（节点=神经元） ----------
    def plot_network_topology(model, save_dir):
        G = nx.DiGraph()  # 有向图（输入→输出）

        # 定义各层神经元节点（修复：使用清晰的中文名称，避免乱码）
        input_nodes = [f'输入层神经元{i+1}' for i in range(3)]
        layer1_nodes = [f'隐藏层1神经元{i+1}' for i in range(3)]
        layer2_nodes = [f'隐藏层2神经元{i+1}' for i in range(2)]
        output_nodes = [f'输出层神经元{i+1}' for i in range(2)]

        # 添加所有节点
        G.add_nodes_from(input_nodes, layer='输入层')
        G.add_nodes_from(layer1_nodes, layer='隐藏层1')
        G.add_nodes_from(layer2_nodes, layer='隐藏层2')
        G.add_nodes_from(output_nodes, layer='输出层')

        # 添加边（输入→隐藏层1），边权重=linear1的weight
        linear1_weight = model.linear1.weight.detach().numpy()
        for i, in_node in enumerate(input_nodes):
            for j, out_node in enumerate(layer1_nodes):
                G.add_edge(in_node, out_node, weight=round(linear1_weight[j, i], 3))

        # 添加边（隐藏层1→隐藏层2）
        linear2_weight = model.linear2.weight.detach().numpy()
        for i, in_node in enumerate(layer1_nodes):
            for j, out_node in enumerate(layer2_nodes):
                G.add_edge(in_node, out_node, weight=round(linear2_weight[j, i], 3))

        # 添加边（隐藏层2→输出层）
        linear3_weight = model.linear3.weight.detach().numpy()
        for i, in_node in enumerate(layer2_nodes):
            for j, out_node in enumerate(output_nodes):
                G.add_edge(in_node, out_node, weight=round(linear3_weight[j, i], 3))

        # 布局：按层排列
        pos = {}
        layer_x = [0, 1, 2, 3]  # 输入层x=0，隐藏层1=x=1，隐藏层2=x=2，输出层=x=3
        layer_y = {
            0: [0, 1, 2],  # 输入层3个神经元的y坐标
            1: [0, 1, 2],  # 隐藏层1 3个神经元
            2: [0.5, 1.5], # 隐藏层2 2个神经元
            3: [0.5, 1.5]  # 输出层 2个神经元
        }
        for i, node in enumerate(input_nodes):
            pos[node] = (layer_x[0], layer_y[0][i])
        for i, node in enumerate(layer1_nodes):
            pos[node] = (layer_x[1], layer_y[1][i])
        for i, node in enumerate(layer2_nodes):
            pos[node] = (layer_x[2], layer_y[2][i])
        for i, node in enumerate(output_nodes):
            pos[node] = (layer_x[3], layer_y[3][i])

        # 绘图
        plt.figure(figsize=(12, 8))
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=['lightblue']*3 + ['lightgreen']*3 + ['orange']*2 + ['red']*2)
        # 绘制边
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        # 边的宽度正比于权重绝对值，颜色区分正负
        edge_colors = ['green' if w > 0 else 'red' for w in weights]
        edge_widths = [abs(w)*2 + 0.5 for w in weights]
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=edge_widths, edge_color=edge_colors, alpha=0.7, arrowsize=20)
        # 绘制节点标签
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        # 绘制边权重标签
        edge_labels = {(u, v): G[u][v]['weight'] for u, v in edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title('神经网络拓扑结构（节点=神经元，边=权重）')
        plt.axis('off')
        # 保存到指定文件夹
        save_path2 = os.path.join(save_dir, '网络拓扑结构.png')
        plt.savefig(save_path2, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"已保存：{save_path2}")

    # 调用拓扑图绘制函数
    plot_network_topology(model, save_dir)

# ===================== 3. 模型训练+可视化（原有逻辑+新增可视化） =====================
def train():
    # 1. 创建模型对象
    my_model = ModelDemo()

    # 2. 创建数据集样本（原有逻辑）
    data = torch.randn(size=(5, 3))
    print(f'data: {data}')
    print(f'data.shape: {data.shape}')
    print(f'data.requires_grad: {data.requires_grad}')

    # 3. 前向传播（原有逻辑）
    output = my_model(data)
    print(f'output: {output}')
    print(f'output.shape: {output.shape}')
    print(f'output.requires_grad: {output.requires_grad}')

    # 4. 查看模型参数（原有逻辑）
    summary(my_model, input_size=(5, 3))
    for name, param in my_model.named_parameters():
        print(f'name: {name}')
        print(f'param: {param}')
        print(f'param.shape: {param.shape}')
        print(f'param.requires_grad: {param.requires_grad}')
        print('-'*50)

    # 5. 新增：调用可视化函数，保存到指定文件夹
    visualize_neurons(my_model, data, SAVE_DIR)

# ===================== 4. 测试入口 =====================
if __name__ == '__main__':
    train()