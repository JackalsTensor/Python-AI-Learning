import pandas as pd
import numpy as np
from copy import deepcopy

# ========== 1. 读取数据 ==========
df = pd.read_csv(r"D:\PythonProject1\数学建模\模拟1\附件1：订单信息.csv")

# ========== 2. 构建订单-货品集合 ==========
order_items = df.groupby('OrderNo')['ItemNo'].apply(set).to_dict()
orders_list = list(order_items.keys())

# ========== 3. 订单货品种类数统计 ==========
order_sizes = [len(order_items[o]) for o in orders_list]

print("=" * 60)
print("【图1 需要填的数据】")
print("=" * 60)
print(f"订单总数: {len(order_sizes)}")
print(f"最小货品种类数: {min(order_sizes)}")
print(f"最大货品种类数: {max(order_sizes)}")
print(f"平均货品种类数: {sum(order_sizes) / len(order_sizes):.2f}")

percentiles = np.percentile(order_sizes, [25, 50, 75])
print(f"25%分位数: {percentiles[0]:.0f}")
print(f"50%分位数: {percentiles[1]:.0f}")
print(f"75%分位数: {percentiles[2]:.0f}")
print(f"大部分订单集中在 {percentiles[0]:.0f} ~ {percentiles[2]:.0f} 之间")

large_orders = [s for s in order_sizes if s > 100]
print(f"超过100种货品的大订单数: {len(large_orders)}")

# ========== 4. 理论下界 ==========
all_items = set()
for items in order_items.values():
    all_items |= items
unique_items_count = len(all_items)
lower_bound = (unique_items_count + 199) // 200

print("\n" + "=" * 60)
print("【理论下界】")
print("=" * 60)
print(f"全局货品种类总数: {unique_items_count}")
print(f"理论下界（最少批次数）: {lower_bound}")


# ========== 5. 贪心分批算法 ==========
def greedy_batching(order_items_dict, orders_sorted=None, N=200):
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


# 运行贪心
batches_greedy = greedy_batching(order_items)
greedy_count = len(batches_greedy)


# ========== 6. 局部交换优化 ==========
def local_search_improvement(order_items_dict, batches, max_iterations=500):
    batches = deepcopy(batches)
    improved = True
    iteration = 0

    while improved and iteration < max_iterations:
        improved = False
        iteration += 1

        for i in range(len(batches)):
            if len(batches[i]['orders']) == 0:
                continue
            for order in batches[i]['orders'][:]:
                order_set = order_items_dict[order]
                for j in range(len(batches)):
                    if i == j:
                        continue
                    new_items_j = batches[j]['items'] | order_set
                    if len(new_items_j) <= 200:
                        remaining_items_i = batches[i]['items'] - order_set
                        batches[i]['orders'].remove(order)
                        batches[i]['items'] = remaining_items_i
                        batches[j]['items'] = new_items_j
                        batches[j]['orders'].append(order)
                        if len(batches[i]['orders']) == 0:
                            batches.pop(i)
                            improved = True
                            break
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break
    return batches


print("\n正在运行局部交换优化...")
batches_improved = local_search_improvement(order_items, batches_greedy, max_iterations=500)
improved_count = len(batches_improved)
improvement = greedy_count - improved_count
improvement_pct = (improvement / greedy_count * 100) if greedy_count > 0 else 0
gap_to_lower = improved_count - lower_bound
gap_pct = (gap_to_lower / lower_bound * 100) if lower_bound > 0 else 0

# ========== 7. 提取优化后的批次数据 ==========
batch_sizes_improved = [len(b['items']) for b in batches_improved]
batch_order_counts_improved = [len(b['orders']) for b in batches_improved]

print("\n" + "=" * 60)
print("【图2/3 需要填的数据（优化后结果）】")
print("=" * 60)
print(f"总批次数: {improved_count}")
print(f"每批种类数 - 最小: {min(batch_sizes_improved)}")
print(f"每批种类数 - 最大: {max(batch_sizes_improved)}")
print(f"每批种类数 - 平均: {sum(batch_sizes_improved) / len(batch_sizes_improved):.2f}")
print(f"每批订单数 - 最小: {min(batch_order_counts_improved)}")
print(f"每批订单数 - 最大: {max(batch_order_counts_improved)}")
print(f"每批订单数 - 平均: {sum(batch_order_counts_improved) / len(batch_order_counts_improved):.2f}")
print(f"每批订单数 - 标准差: {np.std(batch_order_counts_improved):.2f}")

print("\n" + "=" * 60)
print("【图4 需要填的数据（算法对比）】")
print("=" * 60)
print(f"理论下界: {lower_bound}")
print(f"贪心算法批次数: {greedy_count}")
print(f"优化后批次数: {improved_count}")
print(f"减少批次数: {improvement} ({improvement_pct:.1f}%)")
print(f"优化后与下界差距: {gap_to_lower} ({gap_pct:.1f}%)")

# ========== 8. 输出 result1.csv ==========
result_data = []
for group_idx, batch in enumerate(batches_improved, start=1):
    for order in batch['orders']:
        result_data.append({'OrderNo': order, 'GroupNo': group_idx})

result_df = pd.DataFrame(result_data)
result_df.to_csv('result1.csv', index=False, encoding='utf-8')

print("\n" + "=" * 60)
print("【输出文件】")
print("=" * 60)
print(f"已生成 result1.csv，共 {len(result_df)} 行")
print("\n前10行示例：")
print(result_df.head(10))

# ========== 9. 输出论文填空汇总 ==========
print("\n" + "=" * 60)
print("【论文填空汇总 - 直接复制使用】")
print("=" * 60)
print(f"""
【图1填数】
- 订单总数: 923
- 最小货品种类数: {min(order_sizes)}
- 最大货品种类数: {max(order_sizes)}
- 平均货品种类数: {sum(order_sizes) / len(order_sizes):.2f}
- 大部分订单集中在 {percentiles[0]:.0f} ~ {percentiles[2]:.0f} 之间
- 超过100种货品的大订单数: {len(large_orders)}

【理论下界】
- 全局货品种类总数: {unique_items_count}
- 理论下界: {lower_bound}

【图2/3填数（优化后结果）】
- 总批次数: {improved_count}
- 每批种类数 - 最小: {min(batch_sizes_improved)}
- 每批种类数 - 最大: {max(batch_sizes_improved)}
- 每批种类数 - 平均: {sum(batch_sizes_improved) / len(batch_sizes_improved):.2f}
- 每批订单数 - 最小: {min(batch_order_counts_improved)}
- 每批订单数 - 最大: {max(batch_order_counts_improved)}
- 每批订单数 - 平均: {sum(batch_order_counts_improved) / len(batch_order_counts_improved):.2f}
- 每批订单数 - 标准差: {np.std(batch_order_counts_improved):.2f}

【图4填数】
- 理论下界: {lower_bound}
- 贪心算法批次数: {greedy_count}
- 优化后批次数: {improved_count}
- 减少批次数: {improvement} ({improvement_pct:.1f}%)
- 优化后与下界差距: {gap_to_lower} ({gap_pct:.1f}%)
""")