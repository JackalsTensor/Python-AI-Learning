import pandas as pd
import networkx as nx  # 图论建模核心库
import matplotlib.pyplot as plt  # 可选：可视化路径
from matplotlib.lines import Line2D  # 新增：用于添加图例

# 读取预处理后的有效路段数据（路径替换为你的文件路径）
df = pd.read_csv(r"D:\PythonProject1\数学建模\国赛模拟01\预处理后_路段表.csv")
print("有效路段数据预览：")
print(df.head())  # 补充：打印数据预览，方便核对

#步骤 2.2：构建无向路网图
# 1. 创建空地无向图（城市路网无单向通行约束，用无向图）
G = nx.Graph()

# 2. 遍历有效路段，逐个添加到图中
for idx, row in df.iterrows():
    start_node = row["起点"]
    end_node = row["终点"]
    time = row["time"]  # 边的权重：通行时间（小时）
    length = row["length"]  # 可选：保留长度信息，用于后续验证
    h = row["h"]  # 可选：保留积水深度信息

    # 添加边（起点，终点，权重=时间，其他属性按需添加）
    G.add_edge(
        start_node, end_node,
        time=time,
        length=length,
        h=h
    )

# 验证图结构：输出节点数、边数
print(f"\n路网图构建完成：")
print(f"节点总数：{len(G.nodes)}")  # 应接近25个（剔除禁行路段后可能略少）
print(f"有效边数：{len(G.edges)}")  # 应≤38个（原始38条，剔除禁行后减少）

#步骤 2.3：验证路网连通性（关键！）
# 检查节点1和节点20是否在图中
if 1 not in G.nodes or 20 not in G.nodes:
    print("❌ 错误：节点1或节点20不在有效路网中！")
else:
    # 检查两点是否连通
    is_connected = nx.has_path(G, source=1, target=20)
    if not is_connected:
        print("❌ 错误：节点1到节点20无可达路径（禁行路段过多）！")
    else:
        print("✅ 节点1到节点20连通，可求解最短路径。")

#步骤 2.4：调用 Dijkstra 算法求解最短时间路径
# 求解最短时间路径（权重为"time"）
shortest_path = nx.dijkstra_path(G, source=1, target=20, weight="time")
# 求解最短路径的总通行时间
total_time = nx.dijkstra_path_length(G, source=1, target=20, weight="time")

# 输出核心结果
print(f"\n===== 单目标最短路径结果 =====")
print(f"最短时间路径：{shortest_path}")
print(f"总通行时间：{total_time:.4f} 小时")  # 保留4位小数，更精准
print(f"总通行时间（分钟）：{total_time*60:.2f} 分钟")  # 转换为分钟，更易理解

#步骤 2.5：拆解路径明细（验证 + 分析）
print(f"\n===== 路径明细 =====")
path_detail = []  # 存储每段的明细
for i in range(len(shortest_path)-1):
    # 取当前节点和下一个节点
    u = shortest_path[i]
    v = shortest_path[i+1]
    # 获取该路段的属性
    edge_attr = G.edges[u, v]
    # 整理明细
    detail = {
        "路段": f"{u}→{v}",
        "积水深度(cm)": edge_attr["h"],
        "长度(km)": edge_attr["length"],
        "通行速度(km/h)": 40 if edge_attr["h"] <20 else 20,
        "通行时间(h)": edge_attr["time"],
        "通行时间(min)": edge_attr["time"]*60
    }
    path_detail.append(detail)
    # 打印单段信息
    print(f"路段 {u}→{v}：积水{edge_attr['h']}cm | 长度{edge_attr['length']}km | 时间{edge_attr['time']:.4f}h({edge_attr['time']*60:.2f}min)")

# 验证总时间（手动求和，核对算法结果）
manual_total_time = sum([d["通行时间(h)"] for d in path_detail])
print(f"\n手动求和总时间：{manual_total_time:.4f} 小时（与算法结果一致：{abs(manual_total_time-total_time)<1e-6}）")

#步骤 2.6：可视化路径（优化版）
# ========== 核心修改：可视化部分 ==========
# 1. 解决中文乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 替换为你的系统支持的中文字体（如Mac用'Arial Unicode MS'）
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

plt.figure(figsize=(12, 9), dpi=200)  # 增大尺寸+提高分辨率，更清晰
# 绘制整个路网（浅灰色，低透明度，弱化背景）
pos = nx.spring_layout(G, seed=42)  # 固定布局种子，保证图不变
nx.draw(
    G, pos,
    node_size=250,          # 缩小背景节点，突出路径节点
    node_color="#f0f0f0",   # 浅灰色背景节点
    edge_color="#d0d0d0",   # 浅灰色背景边
    alpha=0.4,              # 低透明度，避免抢戏
    with_labels=True,       # 显示节点编号
    font_size=7,            # 缩小字体，更整洁
    font_color="#666666"    # 灰色字体，不刺眼
)

# 绘制最短路径（红色加粗，突出重点）
path_edges = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)]
# 绘制路径边（红色加粗）
nx.draw_networkx_edges(
    G, pos,
    edgelist=path_edges,
    edge_color="#e53e3e",   # 醒目且专业的红色
    width=4,                # 加粗路径边
    alpha=0.8               # 适当透明度
)
# 绘制路径节点（红色，更大尺寸+白色描边）
nx.draw_networkx_nodes(
    G, pos,
    nodelist=shortest_path,
    node_color="#e53e3e",   # 与路径同色
    node_size=450,          # 增大节点尺寸
    edgecolors="white",     # 白色描边，更醒目
    linewidths=2            # 描边宽度
)

# 添加图例（新增：提升专业性）
legend_elements = [
    Line2D([0], [0], color="#e53e3e", lw=4, label="最优路径"),
    Line2D([0], [0], color="#d0d0d0", lw=1, label="普通路段")
]
plt.legend(
    handles=legend_elements,
    loc="upper right",      # 图例位置
    fontsize=10,            # 字体大小
    framealpha=1,           # 图例背景不透明
    shadow=True             # 加阴影，更美观
)

# 添加标题（优化格式，更清晰）
plt.title(
    f"节点1→节点20 最短时间路径\n总通行时间：{total_time:.4f} 小时（{total_time*60:.2f} 分钟）",
    fontsize=14,
    fontweight="bold",      # 加粗标题
    pad=20                  # 标题与图的间距
)
plt.axis("off")  # 隐藏坐标轴
plt.tight_layout()  # 自动调整布局，避免文字被截断
plt.savefig(
    "最短路径可视化_优化版.png",
    dpi=300,                # 高清分辨率，适合论文
    bbox_inches="tight",    # 裁剪空白区域
    facecolor="white"       # 白色背景，避免透明
)
plt.show()

#步骤 2.7：结果归档（比赛必备）
# 1. 保存核心结果
result_df = pd.DataFrame({
    "最短路径": [shortest_path],
    "总通行时间(小时)": [total_time],
    "总通行时间(分钟)": [total_time*60]
})
result_df.to_csv("单目标最短路径结果.csv", index=False, encoding="utf-8")

# 2. 保存路径明细
detail_df = pd.DataFrame(path_detail)
detail_df.to_csv("单目标路径明细.csv", index=False, encoding="utf-8")

print(f"\n✅ 结果已保存为CSV文件，可直接用于论文/报告！")