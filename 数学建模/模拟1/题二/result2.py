import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.sparse.linalg import eigsh

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 1. 读取数据 ==========
df_order_items = pd.read_csv(r'D:\PythonProject1\数学建模\模拟1\附件1：订单信息.csv')
df_result1 = pd.read_csv(r'D:\PythonProject1\数学建模\模拟1\题一\result1.csv')  # 第1问的输出

# 构建订单 → 货品集合
order_items = df_order_items.groupby('OrderNo')['ItemNo'].apply(set).to_dict()

# 构建订单 → 批次号
order_to_group = dict(zip(df_result1['OrderNo'], df_result1['GroupNo']))

# 获取所有批次号
groups = sorted(df_result1['GroupNo'].unique())

print("=" * 60)
print("正在计算第2问结果...")
print("=" * 60)


# ========== 2. 谱排序函数 ==========
def spectral_ordering(items_list, orders_in_batch, order_items, item_to_idx):
    """谱排序：返回排序后的货品列表"""
    m = len(items_list)
    if m <= 1:
        return items_list

    # 构建共现矩阵
    C = np.zeros((m, m))
    for oid in orders_in_batch:
        items = list(order_items[oid])
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i] in item_to_idx and items[j] in item_to_idx:
                    u = item_to_idx[items[i]]
                    v = item_to_idx[items[j]]
                    C[u, v] += 1
                    C[v, u] += 1

    # 构建拉普拉斯矩阵
    D = np.diag(C.sum(axis=1))
    L = D - C

    try:
        eigvals, eigvecs = eigsh(L, k=2, which='SM')
        fiedler = eigvecs[:, 1] if len(eigvals) > 1 else eigvecs[:, 0]
    except:
        fiedler = np.arange(m)

    sorted_indices = np.argsort(fiedler)
    return [items_list[i] for i in sorted_indices]


def greedy_ordering(items_list, orders_in_batch, order_items, item_to_idx):
    """贪心排序：按共现频率贪心"""
    if len(items_list) <= 1:
        return items_list

    m = len(items_list)
    # 构建共现矩阵
    C = np.zeros((m, m))
    for oid in orders_in_batch:
        items = list(order_items[oid])
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i] in item_to_idx and items[j] in item_to_idx:
                    u = item_to_idx[items[i]]
                    v = item_to_idx[items[j]]
                    C[u, v] += 1
                    C[v, u] += 1

    # 贪心：从出现次数最多的货品开始
    degrees = C.sum(axis=1)
    start = np.argmax(degrees)
    used = [start]
    remaining = list(set(range(m)) - {start})

    while remaining:
        last = used[-1]
        # 找与最后一个货品共现次数最高的
        best = max(remaining, key=lambda x: C[last, x])
        used.append(best)
        remaining.remove(best)

    return [items_list[i] for i in used]


def random_ordering(items_list, _1, _2, _3):
    """随机排序作为基线"""
    import random
    shuffled = items_list.copy()
    random.shuffle(shuffled)
    return shuffled


def compute_batch_distance(orders_in_batch, order_items, shelf_mapping, items_in_batch):
    """计算一个批次的总拣选距离"""
    total = 0
    for oid in orders_in_batch:
        shelves = [shelf_mapping[item] for item in order_items[oid] if item in shelf_mapping]
        if shelves:
            total += max(shelves) - min(shelves)
    return total


# ========== 3. 对每个批次运行三种算法，收集结果 ==========
results = {name: [] for name in ['random', 'greedy', 'spectral']}
batch_distances = {name: {} for name in ['random', 'greedy', 'spectral']}
batch_shelf_mappings = {}  # 存储谱排序的货架映射（用于输出result2.csv）

for group_id in groups:
    print(f"处理批次 {group_id}...")

    # 获取该批次的所有订单
    orders_in_batch = [oid for oid, g in order_to_group.items() if g == group_id]

    # 提取该批次所有货品
    items_in_batch = set()
    for oid in orders_in_batch:
        items_in_batch |= order_items[oid]
    items_list = list(items_in_batch)
    m = len(items_list)

    if m == 0:
        continue

    item_to_idx = {item: i for i, item in enumerate(items_list)}

    # 三种排序方法
    for method_name, method_func in [('random', random_ordering),
                                     ('greedy', greedy_ordering),
                                     ('spectral', spectral_ordering)]:
        sorted_items = method_func(items_list, orders_in_batch, order_items, item_to_idx)
        shelf_mapping = {item: idx + 1 for idx, item in enumerate(sorted_items)}
        total_dist = compute_batch_distance(orders_in_batch, order_items, shelf_mapping, items_in_batch)
        results[method_name].append(total_dist)
        batch_distances[method_name][group_id] = total_dist

    # 保存谱排序的货架映射（用于输出result2.csv）
    sorted_items = spectral_ordering(items_list, orders_in_batch, order_items, item_to_idx)
    shelf_mapping = {item: idx + 1 for idx, item in enumerate(sorted_items)}
    for item in items_list:
        batch_shelf_mappings[(item, group_id)] = shelf_mapping[item]

# ========== 图 A：高频货品共现热力图 ==========
print("\n生成图 A：高频货品共现热力图...")

# 统计每个货品出现的次数（在多少订单中出现）
item_freq = df_order_items.groupby('ItemNo')['OrderNo'].nunique().sort_values(ascending=False)
top_n = 20
top_items = item_freq.head(top_n).index.tolist()

# 构建共现矩阵
df_top = df_order_items[df_order_items['ItemNo'].isin(top_items)]
order_top_items = df_top.groupby('OrderNo')['ItemNo'].apply(set).to_dict()
cooc_matrix = pd.DataFrame(0, index=top_items, columns=top_items)
for order, items in order_top_items.items():
    items_list = list(items)
    for i in range(len(items_list)):
        for j in range(i + 1, len(items_list)):
            a, b = items_list[i], items_list[j]
            cooc_matrix.loc[a, b] += 1
            cooc_matrix.loc[b, a] += 1
for item in top_items:
    cooc_matrix.loc[item, item] = 0

plt.figure(figsize=(14, 12))
sns.heatmap(cooc_matrix, annot=True, fmt='d', cmap='YlOrRd',
            linewidths=0.5, linecolor='gray', square=True,
            cbar_kws={'label': '共现次数'})
plt.title(f'高频货品共现热力图 (TOP {top_n})', fontsize=16)
plt.xlabel('货品编号', fontsize=12)
plt.ylabel('货品编号', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('图A_高频货品共现热力图.png', dpi=300, bbox_inches='tight')
plt.show()

# ========== 图 B：算法对比柱状图 ==========
print("\n生成图 B：算法对比柱状图...")

methods = ['随机摆放', '贪心排序', '谱排序']
total_distances = [sum(results['random']), sum(results['greedy']), sum(results['spectral'])]

plt.figure(figsize=(8, 6))
bars = plt.bar(methods, total_distances, color=['gray', 'steelblue', 'green'], edgecolor='black', alpha=0.8)
for bar, val in zip(bars, total_distances):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
             f'{int(val)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.ylabel('所有批次拣选距离总和', fontsize=12)
plt.title('算法对比', fontsize=14)
plt.grid(axis='y', alpha=0.3)
improve_greedy = (total_distances[0] - total_distances[1]) / total_distances[0] * 100
improve_spectral = (total_distances[0] - total_distances[2]) / total_distances[0] * 100
plt.text(0.02, 0.95,
         f'贪心较随机改善: {improve_greedy:.1f}%\n'
         f'谱排序较随机改善: {improve_spectral:.1f}%',
         transform=plt.gca().transAxes, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
plt.tight_layout()
plt.savefig('图B_算法对比柱状图.png', dpi=300, bbox_inches='tight')
plt.show()

# ========== 图 C：各批次拣选距离分布 ==========
print("\n生成图 C：各批次拣选距离分布...")

spectral_batch_distances = batch_distances['spectral']
batch_ids = sorted(spectral_batch_distances.keys())
batch_dist_vals = [spectral_batch_distances[b] for b in batch_ids]
avg_dist = sum(batch_dist_vals) / len(batch_dist_vals)

plt.figure(figsize=(14, 6))
plt.bar(range(1, len(batch_ids) + 1), batch_dist_vals, color='steelblue', edgecolor='black', alpha=0.7)
plt.axhline(y=avg_dist, color='red', linestyle='--', linewidth=2, label=f'平均距离 = {avg_dist:.1f}')
plt.xlabel('批次编号', fontsize=12)
plt.ylabel('拣选距离总和', fontsize=12)
plt.title('各批次拣选距离分布', fontsize=14)
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.text(0.02, 0.95,
         f'总批次数: {len(batch_ids)}\n'
         f'距离范围: {min(batch_dist_vals)} ~ {max(batch_dist_vals)}',
         transform=plt.gca().transAxes, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
plt.savefig('图C_各批次拣选距离分布.png', dpi=300, bbox_inches='tight')
plt.show()

# ========== 图 D：某代表性批次的订单区间分布 ==========
print("\n生成图 D：代表性批次的订单区间分布...")

# 选择一个订单数适中的代表性批次（比如订单数在15-25之间的第一个批次）
rep_batch = None
for g in batch_ids:
    orders_in_batch = [oid for oid, gid in order_to_group.items() if gid == g]
    if 15 <= len(orders_in_batch) <= 25:
        rep_batch = g
        break
if rep_batch is None:
    rep_batch = batch_ids[0]

print(f"选择批次 {rep_batch} 作为代表性批次")

# 获取该批次的信息
orders_in_batch = [oid for oid, g in order_to_group.items() if g == rep_batch]
items_in_batch = set()
for oid in orders_in_batch:
    items_in_batch |= order_items[oid]
items_list = list(items_in_batch)

# 获取谱排序后的货架映射
shelf_mapping = {item: batch_shelf_mappings.get((item, rep_batch), i + 1)
                 for i, item in enumerate(items_list)}

# 计算每个订单的区间
intervals = []
for oid in orders_in_batch:
    shelves = [shelf_mapping[item] for item in order_items[oid] if item in shelf_mapping]
    if shelves:
        intervals.append({
            'order': oid,
            'min': min(shelves),
            'max': max(shelves),
            'length': max(shelves) - min(shelves)
        })

# 按区间长度排序
intervals.sort(key=lambda x: x['length'])

plt.figure(figsize=(12, 8))
for i, interval in enumerate(intervals):
    plt.hlines(y=i, xmin=interval['min'], xmax=interval['max'],
               linewidth=2, color='steelblue', alpha=0.7)
    plt.plot(interval['min'], i, 'go', markersize=4)  # 左端点
    plt.plot(interval['max'], i, 'ro', markersize=4)  # 右端点

plt.xlabel('货架编号', fontsize=12)
plt.ylabel('订单编号（按区间长度排序）', fontsize=12)
plt.title(f'批次 {rep_batch} 订单拣选区间分布（谱排序）', fontsize=14)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('图D_代表性批次订单区间分布.png', dpi=300, bbox_inches='tight')
plt.show()

# ========== 输出 result2.csv ==========
result2_data = []
for (item, group_id), shelf_no in batch_shelf_mappings.items():
    result2_data.append({'ItemNo': item, 'GroupNo': group_id, 'ShelfNo': shelf_no})
df_result2 = pd.DataFrame(result2_data)
df_result2.to_csv('result2.csv', index=False, encoding='utf-8')

# ========== 结果汇总 ==========
print("\n" + "=" * 60)
print("【第2问结果汇总】")
print("=" * 60)
print(f"随机摆放总距离: {sum(results['random']):.0f}")
print(f"贪心排序总距离: {sum(results['greedy']):.0f}")
print(f"谱排序总距离: {sum(results['spectral']):.0f}")
print(f"谱排序较随机改善: {(sum(results['random']) - sum(results['spectral'])) / sum(results['random']) * 100:.1f}%")
print(f"已生成 result2.csv，共 {len(result2_data)} 行")