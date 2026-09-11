import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 1. 读取数据 ==========
df = pd.read_csv(r"D:\PythonProject1\数学建模\模拟1\附件1：订单信息.csv")

# ========== 2. 构建每个订单的货品集合 ==========
order_items = df.groupby('OrderNo')['ItemNo'].apply(set).to_dict()

# 订单列表（按货品种类数降序排序，贪心策略）
orders_sorted = sorted(order_items.keys(),
                       key=lambda o: len(order_items[o]),
                       reverse=True)

# ========== 3. 贪心分批 ==========
batches = []  # 每个元素是一个 dict: {'items': set(), 'orders': []}

for order in orders_sorted:
    order_set = order_items[order]
    placed = False

    # 尝试放入已有批次
    for batch in batches:
        # 计算合并后的种类数
        union_size = len(batch['items'] | order_set)
        if union_size <= 200:
            batch['items'] |= order_set
            batch['orders'].append(order)
            placed = True
            break

    # 如果放不进任何已有批次，创建新批次
    if not placed:
        batches.append({
            'items': order_set.copy(),
            'orders': [order]
        })

# ========== 4. 提取每个批次的货品种类数 ==========
batch_sizes = [len(batch['items']) for batch in batches]
batch_order_counts = [len(batch['orders']) for batch in batches]

# ========== 5. 打印统计信息 ==========
print(f"总批次数: {len(batches)}")
print(
    f"每批种类数 - 最小: {min(batch_sizes)}, 最大: {max(batch_sizes)}, 平均: {sum(batch_sizes) / len(batch_sizes):.2f}")
print(
    f"每批订单数 - 最小: {min(batch_order_counts)}, 最大: {max(batch_order_counts)}, 平均: {sum(batch_order_counts) / len(batch_order_counts):.2f}")

# ========== 6. 画图：各批次货品种类数 ==========
plt.figure(figsize=(14, 6))

# 柱状图
plt.bar(range(1, len(batch_sizes) + 1), batch_sizes, color='steelblue', edgecolor='black', alpha=0.7)

# 红色虚线：容量上限 200
plt.axhline(y=200, color='red', linestyle='--', linewidth=2, label='容量上限 N=200')

# 标题和标签
plt.xlabel('批次编号', fontsize=12)
plt.ylabel('货品种类数', fontsize=12)
plt.title('各批次货品种类数分布', fontsize=14)

# 添加图例
plt.legend()

# 添加网格
plt.grid(axis='y', alpha=0.3)

# 在图上显示统计信息
plt.text(0.02, 0.95,
         f'总批次数: {len(batches)}\n'
         f'平均种类数: {sum(batch_sizes) / len(batch_sizes):.1f}\n'
         f'种类数范围: {min(batch_sizes)} ~ {max(batch_sizes)}',
         transform=plt.gca().transAxes,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()

# 保存图片
plt.savefig('图2_各批次货品种类数分布.png', dpi=300, bbox_inches='tight')

# 显示
plt.show()