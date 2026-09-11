import networkx as nx

# 1. 构建图
G = nx.Graph()
# 2. 添加有效路段（示例：需替换为实际数据）
# 格式：G.add_edge(起点, 终点, time=通行时间, length=长度, h=积水深度)
G.add_edge(1,2, time=0.05, length=0.2, h=15)
G.add_edge(2,3, time=0.1, length=0.2, h=25)
# ... 补充所有有效路段
# 3. 求解最短时间路径
shortest_path = nx.dijkstra_path(G, source=1, target=20, weight='time')
shortest_time = nx.dijkstra_path_length(G, source=1, target=20, weight='time')
# 4. 输出结果
print("最短时间路径：", shortest_path)
print("最短通行时间：", shortest_time, "小时")
