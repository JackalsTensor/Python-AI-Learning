import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 1. 读取数据 ==========
df = pd.read_csv(r"D:\PythonProject1\数学建模\模拟1\附件1：订单信息.csv")

# ========== 2. 构建每个订单的货品集合 ==========
order_items = df.groupby('OrderNo')['ItemNo'].apply(set).to_dict()
orders_list = list(order_items.keys())

# ========== 3. 计算理论下界 ==========
# 所有货品去重后的总数
all_items = set()
for items in order_items.values():
    all_items |= items
unique_items_count = len(all_items)
lower_bound = (unique_items_count + 199) // 200  # 向上取整

print(f"全局货品种类总数: {unique_items_count}")
print(f"理论下界（最少批次数）: {lower_bound}")


# ========== 4. 贪心分批算法 ==========
def greedy_batching(order_items_dict, orders_sorted=None, N=200):
    """贪心分批，返回 batches 列表"""
    if orders_sorted is None:
        orders_sorted = sorted(order_items_dict.keys(),
                               key=lambda o: len(order_items_dict[o]),
                               reverse=True)

    batches = []
    for order in orders_sorted:
        order_set = order_items_dict[order]
        placed = False

        for batch in batches:
            union_size = len(batch['items'] | order_set)
            if union_size <= N:
                batch['items'] |= order_set
                batch['orders'].append(order)
                placed = True
                break

        if not placed:
            batches.append({
                'items': order_set.copy(),
                'orders': [order]
            })

    return batches


# 运行贪心算法
batches_greedy = greedy_batching(order_items)
greedy_count = len(batches_greedy)
print(f"贪心算法批次数: {greedy_count}")


# ========== 5. 局部交换优化 ==========
def local_search_improvement(order_items_dict, batches, max_iterations=1000):
    """
    局部交换优化：
    尝试将一个订单从当前批次移动到另一个批次
    如果能减少批次数，则接受
    """
    batches = deepcopy(batches)
    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        # 遍历每个批次中的每个订单
        for i in range(len(batches)):
            if len(batches[i]['orders']) == 0:
                continue

            for order in batches[i]['orders'][:]:  # 复制列表，避免迭代时修改
                order_set = order_items_dict[order]

                # 尝试将订单移到其他批次
                for j in range(len(batches)):
                    if i == j:
                        continue

                    # 计算移到 j 批次后的种类数
                    new_items_j = batches[j]['items'] | order_set
                    if len(new_items_j) <= 200:
                        # 计算移除订单后 i 批次的种类数
                        remaining_items_i = batches[i]['items'] - order_set

                        # 如果 i 批次变空，可以删除该批次
                        batches[i]['orders'].remove(order)
                        batches[i]['items'] = remaining_items_i
                        batches[j]['items'] = new_items_j
                        batches[j]['orders'].append(order)

                        # 如果 i 批次变空，删除它
                        if len(batches[i]['orders']) == 0:
                            batches.pop(i)
                            # 注意：删除了一个批次，索引变化，需要重新开始
                            improved = True
                            break

                        improved = True
                        break

                if improved:
                    break

            if improved:
                break

    return batches


# 运行局部搜索优化
print("正在进行局部交换优化...")
batches_improved = local_search_improvement(order_items, batches_greedy, max_iterations=500)
improved_count = len(batches_improved)
print(f"优化后批次数: {improved_count}")
print(f"减少批次数: {greedy_count - improved_count}")

# ========== 6. 画图：算法对比柱状图 ==========
methods = ['理论下界', '贪心算法', '贪心+局部交换']
values = [lower_bound, greedy_count, improved_count]

# 计算提升百分比
improvement_pct = (greedy_count - improved_count) / greedy_count * 100 if greedy_count > 0 else 0
gap_to_lower = (improved_count - lower_bound) / lower_bound * 100 if lower_bound > 0 else 0

plt.figure(figsize=(8, 6))

# 柱状图
bars = plt.bar(methods, values,
               color=['gray', 'steelblue', 'green'],
               edgecolor='black',
               alpha=0.8)

# 在柱子上方显示数值
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             str(val), ha='center', va='bottom', fontsize=12, fontweight='bold')

# 标题和标签
plt.ylabel('批次数', fontsize=12)
plt.title('算法批次数对比', fontsize=14)

# 添加网格
plt.grid(axis='y', alpha=0.3)

# 添加说明文字
plt.text(0.02, 0.95,
         f'贪心 → 优化减少: {greedy_count - improved_count} 批次 ({improvement_pct:.1f}%)\n'
         f'优化后与下界差距: {gap_to_lower:.1f}%\n'
         f'(下界 = ceil({unique_items_count}/200) = {lower_bound})',
         transform=plt.gca().transAxes,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7),
         fontsize=10)

plt.tight_layout()

# 保存图片
plt.savefig('图4_算法批次数对比.png', dpi=300, bbox_inches='tight')

# 显示
plt.show()

# ========== 7. 额外：优化前后批次种类数分布对比 ==========
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 贪心结果
batch_sizes_greedy = [len(b['items']) for b in batches_greedy]
axes[0].bar(range(1, len(batch_sizes_greedy) + 1), batch_sizes_greedy, color='steelblue', alpha=0.7)
axes[0].axhline(y=200, color='red', linestyle='--', label='N=200')
axes[0].set_xlabel('批次编号')
axes[0].set_ylabel('货品种类数')
axes[0].set_title('贪心算法 - 各批次种类数')
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# 优化后结果
batch_sizes_improved = [len(b['items']) for b in batches_improved]
axes[1].bar(range(1, len(batch_sizes_improved) + 1), batch_sizes_improved, color='green', alpha=0.7)
axes[1].axhline(y=200, color='red', linestyle='--', label='N=200')
axes[1].set_xlabel('批次编号')
axes[1].set_ylabel('货品种类数')
axes[1].set_title('贪心+局部交换 - 各批次种类数')
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('图4_附加_优化前后批次数对比.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n===== 结果汇总 =====")
print(f"理论下界: {lower_bound}")
print(f"贪心算法批次数: {greedy_count}")
print(f"优化后批次数: {improved_count}")
print(f"优化幅度: {greedy_count - improved_count} 批次 ({improvement_pct:.1f}%)")