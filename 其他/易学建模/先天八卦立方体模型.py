import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ========== 1. 解决中文乱码问题 ==========
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 优先黑体，支持中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# ========== 2. 定义八卦坐标、名称和颜色 ==========
gua_data = [
    (0, 0, 0, "坤", "blue"),
    (1, 0, 0, "震", "red"),
    (0, 1, 0, "坎", "red"),
    (1, 1, 0, "兑", "blue"),
    (0, 0, 1, "艮", "red"),
    (1, 0, 1, "离", "blue"),
    (0, 1, 1, "巽", "blue"),
    (1, 1, 1, "乾", "green"),  # 乾卦高亮绿色
]

# 立方体的边连接关系
edges = [
    [0, 1], [0, 2], [1, 3], [2, 3],  # 底面 z=0
    [4, 5], [4, 6], [5, 7], [6, 7],  # 顶面 z=1
    [0, 4], [1, 5], [2, 6], [3, 7]  # 竖棱
]

# ========== 3. 创建3D画布 ==========
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制立方体的边
for edge in edges:
    p1 = gua_data[edge[0]]
    p2 = gua_data[edge[1]]
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='blue', linewidth=2)

# ========== 4. 绘制点 + 标注卦名和坐标 ==========
for x, y, z, name, color in gua_data:
    # 绘制点
    ax.scatter(x, y, z, color=color, s=120, zorder=5)  # zorder=5 让点显示在线的前面

    # 标注文字：卦名 + 坐标，位置偏移避免被挡住
    ax.text(
        x + 0.06, y + 0.06, z + 0.06,  # 文字偏移一点，不被点挡住
        f"{name}\n({x},{y},{z})",
        fontsize=12,
        color='black',
        weight='bold',  # 加粗文字更清晰
        zorder=10  # 让文字显示在最上层
    )

# ========== 5. 设置坐标轴和标题 ==========
ax.set_xlabel('X 轴', fontsize=14)
ax.set_ylabel('Y 轴', fontsize=14)
ax.set_zlabel('Z 轴', fontsize=14)
ax.set_xlim(-0.3, 1.3)
ax.set_ylim(-0.3, 1.3)
ax.set_zlim(-0.3, 1.3)

# 调整视角，和原图一致
ax.view_init(elev=25, azim=-45)

# 设置标题
plt.title('先天八卦 三维立方体模型', fontsize=18, weight='bold', pad=20)

plt.tight_layout()
plt.show()