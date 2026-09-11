"""
目的：展示数据特征，解释为什么用降序贪心
X 轴：订单的货品种类数
Y 轴：订单数量
你需要的数据：
• 每个订单的 len(set(items))
"""

import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体（解决中文显示问题）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 1. 读取数据 ==========
df = pd.read_csv(r"D:\PythonProject1\数学建模\模拟1\附件1：订单信息.csv")

# ========== 2. 统计每个订单的货品种类数 ==========
# 按订单编号分组，用 nunique() 统计每个订单中不重复的货品种类数
order_items_count = df.groupby('OrderNo')['ItemNo'].nunique()

# 转换为列表（用于画图）
order_sizes = order_items_count.tolist()

# ========== 3. 打印统计信息（可选） ==========
print(f"订单总数: {len(order_sizes)}")
print(f"最小种类数: {min(order_sizes)}")
print(f"最大种类数: {max(order_sizes)}")
print(f"平均种类数: {sum(order_sizes)/len(order_sizes):.2f}")

# ========== 4. 画直方图 ==========
plt.figure(figsize=(10, 6))
plt.hist(order_sizes, bins=30, edgecolor='black', alpha=0.7, color='steelblue')

# 添加标题和标签
plt.xlabel('订单货品种类数', fontsize=12)
plt.ylabel('订单数量', fontsize=12)
plt.title('订单货品种类数分布直方图', fontsize=14)

# 添加网格（增加可读性）
plt.grid(axis='y', alpha=0.3)

# 显示统计信息在图上
plt.text(0.7, 0.95,
         f'订单总数: {len(order_sizes)}\n'
         f'最大种类: {max(order_sizes)}\n'
         f'平均种类: {sum(order_sizes)/len(order_sizes):.2f}',
         transform=plt.gca().transAxes,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()

# ========== 5. 保存图片（建议） ==========
plt.savefig('图1_订单货品种类数分布.png', dpi=300, bbox_inches='tight')

# 显示图片
plt.show()