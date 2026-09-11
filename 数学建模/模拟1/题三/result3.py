import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 1. 读取数据 ==========
print("=" * 60)
print("第3问：分拣任务指派")
print("=" * 60)

# 读取订单-货品数据
df_items = pd.read_csv(r'D:\PythonProject1\数学建模\模拟1\附件1：订单信息.csv')

# 读取第1问结果（订单→批次）
df_result1 = pd.read_csv(r'D:\PythonProject1\数学建模\模拟1\题一\result1.csv')

# 读取第2问结果（货品→批次→货架）
df_result2 = pd.read_csv(r'D:\PythonProject1\数学建模\模拟1\题二\result2.csv')

# ========== 2. 构建必要的数据结构 ==========
# 订单 → 货品集合
order_items = df_items.groupby('OrderNo')['ItemNo'].apply(set).to_dict()

# 订单 → 批次号
order_to_group = dict(zip(df_result1['OrderNo'], df_result1['GroupNo']))

# 货品 → (批次, 货架)
item_to_shelf = {}
for _, row in df_result2.iterrows():
    item_to_shelf[(row['ItemNo'], row['GroupNo'])] = row['ShelfNo']

# 获取所有批次号
groups = sorted(df_result1['GroupNo'].unique())
print(f"总批次数: {len(groups)}")


# ========== 3. 计算每个订单的货架区间 ==========
def get_order_interval(order, group):
    """返回订单的货架区间 [L, R]"""
    items = order_items.get(order, set())
    shelves = []
    for item in items:
        shelf = item_to_shelf.get((item, group))
        if shelf is not None:
            shelves.append(shelf)
    if not shelves:
        return None
    return (min(shelves), max(shelves))


# 存储每个订单的区间
order_intervals = {}
for order, group in order_to_group.items():
    interval = get_order_interval(order, group)
    if interval:
        order_intervals[order] = {
            'group': group,
            'L': interval[0],
            'R': interval[1],
            'length': interval[1] - interval[0]
        }

print(f"有区间数据的订单数: {len(order_intervals)}")


# ========== 4. 订单距离计算函数 ==========
def compute_order_distance(L, R, current_pos):
    """
    计算从一个订单走到另一个订单的距离
    当前在 current_pos，要处理区间 [L, R]
    返回：行走距离，以及处理完后的位置
    """
    # 先走到区间较近的一端
    dist_to_L = abs(L - current_pos)
    dist_to_R = abs(R - current_pos)
    dist_to_enter = min(dist_to_L, dist_to_R)

    # 然后遍历整个区间
    travel = dist_to_enter + (R - L)

    # 处理完后的位置：如果从L进入，结束在R；如果从R进入，结束在L
    if dist_to_L <= dist_to_R:
        end_pos = R
    else:
        end_pos = L

    return travel, end_pos


# ========== 5. 贪心指派算法 ==========
def assign_orders_greedy(orders_in_batch, order_intervals, n_workers=5):
    """
    贪心指派：每次将订单分配给当前总时间最小的工人
    返回：assignment (订单 → (worker, task_no)), 每个工人的总距离和位置
    """
    # 初始化工人
    workers = {
        w: {
            'total_distance': 0,
            'current_pos': 1,  # 从1号货架出发
            'orders': []  # (order, task_no)
        } for w in range(1, n_workers + 1)
    }

    # 按订单的区间长度排序（可选，尝试不同策略）
    # 这里按原始顺序（即批次内的自然顺序）
    assignment = {}

    for order in orders_in_batch:
        interval = order_intervals[order]
        L, R = interval['L'], interval['R']

        # 计算每个工人处理该订单后的总时间
        best_worker = None
        best_new_total = float('inf')

        for w in range(1, n_workers + 1):
            travel, _ = compute_order_distance(L, R, workers[w]['current_pos'])
            new_total = workers[w]['total_distance'] + travel
            if new_total < best_new_total:



                best_new_total = new_total
                best_worker = w

        # 分配订单
        w = best_worker
        travel, new_pos = compute_order_distance(L, R, workers[w]['current_pos'])
        workers[w]['total_distance'] += travel
        workers[w]['current_pos'] = new_pos
        task_no = len(workers[w]['orders']) + 1
        workers[w]['orders'].append((order, task_no))
        assignment[order] = (w, task_no)

    return assignment, workers


# ========== 6. 对每个批次执行指派 ==========
print("\n正在执行订单指派...")

all_assignments = []  # 存储 (order, group, worker, task_no)
batch_completion_times = {}  # 每个批次的完成时间（最大工人时间）
worker_distances_by_batch = defaultdict(list)  # 每个工人每批次的距离

for group in groups:
    # 获取该批次的所有订单
    orders_in_batch = [order for order, g in order_to_group.items() if g == group]
    # 只保留有区间数据的订单
    orders_in_batch = [o for o in orders_in_batch if o in order_intervals]

    if not orders_in_batch:
        continue

    # 贪心指派
    assignment, workers = assign_orders_greedy(orders_in_batch, order_intervals, n_workers=5)

    # 记录批次的完成时间（最大工人距离）
    max_time = max(workers[w]['total_distance'] for w in workers)
    batch_completion_times[group] = max_time

    # 记录每个工人的距离
    for w in workers:
        worker_distances_by_batch[group].append(workers[w]['total_distance'])

    # 存储指派结果
    for order in orders_in_batch:
        w, task_no = assignment[order]
        all_assignments.append({
            'OrderNo': order,
            'GroupNo': group,
            'WorkerNo': w,
            'TaskNo': task_no
        })

# ========== 7. 计算全局结果 ==========
df_result3 = pd.DataFrame(all_assignments)

# 计算每个工人的总距离（所有批次累加）
worker_total_distances = defaultdict(float)
for _, row in df_result3.iterrows():
    w = row['WorkerNo']
    # 需要从 order_intervals 获取该订单的距离？不对，这里我们应该从批次结果中累加
    # 更简单：重新计算每个工人的总距离

# 重新计算每个工人的总距离
worker_total = {w: 0 for w in range(1, 6)}
worker_by_group = defaultdict(lambda: defaultdict(list))

for group in groups:
    orders_in_batch = [order for order, g in order_to_group.items() if g == group]
    orders_in_batch = [o for o in orders_in_batch if o in order_intervals]
    if not orders_in_batch:
        continue

    # 重新模拟该批次
    workers = {w: {'total_distance': 0, 'current_pos': 1} for w in range(1, 6)}

    for order in orders_in_batch:
        w = df_result3[df_result3['OrderNo'] == order]['WorkerNo'].values[0]
        interval = order_intervals[order]
        travel, new_pos = compute_order_distance(interval['L'], interval['R'], workers[w]['current_pos'])
        workers[w]['total_distance'] += travel
        workers[w]['current_pos'] = new_pos

    for w in range(1, 6):
        worker_total[w] += workers[w]['total_distance']

# 最大完工时间 = 最慢工人的总距离
makespan = max(worker_total.values())

print("\n" + "=" * 60)
print("【第3问结果汇总】")
print("=" * 60)
print(f"总订单数: {len(df_result3)}")
print(f"总批次数: {len(groups)}")
print(f"分拣工人数: 5")
print(f"\n各工人总运动距离:")
for w in range(1, 6):
    print(f"  工人 {w}: {worker_total[w]:.0f}")
print(f"\n最大完工时间 (makespan): {makespan:.0f}")

# 计算负载均衡指标
distances_list = list(worker_total.values())
mean_dist = np.mean(distances_list)
std_dist = np.std(distances_list)
max_min_ratio = max(distances_list) / min(distances_list) if min(distances_list) > 0 else 0

print(f"\n负载均衡指标:")
print(f"  平均距离: {mean_dist:.0f}")
print(f"  标准差: {std_dist:.2f}")
print(f"  最大/最小比值: {max_min_ratio:.2f}")

# ========== 8. 输出 result3.csv ==========
df_result3 = df_result3.sort_values(['GroupNo', 'WorkerNo', 'TaskNo'])
df_result3.to_csv('result3.csv', index=False, encoding='utf-8')
print(f"\n已生成 result3.csv，共 {len(df_result3)} 行")

# ========== 9. 图 E：各工人任务量对比 ==========
print("\n生成图 E：各工人任务量对比...")

worker_order_counts = df_result3.groupby('WorkerNo').size()

plt.figure(figsize=(10, 6))
bars = plt.bar(worker_order_counts.index, worker_order_counts.values,
               color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
               edgecolor='black', alpha=0.8)
for bar, val in zip(bars, worker_order_counts.values):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
             str(val), ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.xlabel('分拣工编号', fontsize=12)
plt.ylabel('处理订单数量', fontsize=12)
plt.title('图E：各分拣工任务量对比', fontsize=14)
plt.xticks(range(1, 6))
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('图E_各工人任务量对比.png', dpi=300, bbox_inches='tight')
plt.show()

# ========== 10. 图 F：各工人运动距离对比 ==========
plt.figure(figsize=(10, 6))
bars = plt.bar(range(1, 6), [worker_total[w] for w in range(1, 6)],
               color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
               edgecolor='black', alpha=0.8)
for bar, val in zip(bars, [worker_total[w] for w in range(1, 6)]):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
             f'{int(val)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.axhline(y=mean_dist, color='red', linestyle='--', linewidth=2, label=f'平均 = {mean_dist:.0f}')
plt.xlabel('分拣工编号', fontsize=12)
plt.ylabel('运动距离', fontsize=12)
plt.title('图F：各分拣工运动距离对比', fontsize=14)
plt.xticks(range(1, 6))
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('图F_各工人运动距离对比.png', dpi=300, bbox_inches='tight')
plt.show()

# ========== 11. 图 G：甘特图（按批次展示工人任务） ==========
print("\n生成图 G：甘特图...")

# 选择一个代表性的批次（任务最多的批次）
batch_order_counts = df_result3.groupby('GroupNo').size()
rep_batch = batch_order_counts.idxmax()
print(f"选择批次 {rep_batch} 作为甘特图展示")

# 获取该批次的指派结果
batch_assignments = df_result3[df_result3['GroupNo'] == rep_batch]
# 获取该批次订单的区间信息（用于排序）
batch_orders = batch_assignments['OrderNo'].tolist()
batch_intervals = {order: order_intervals[order] for order in batch_orders if order in order_intervals}

# 计算每个工人该批次的订单顺序和累积时间
fig, ax = plt.subplots(figsize=(14, 8))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
worker_colors = {w: colors[i] for i, w in enumerate(range(1, 6))}

y_labels = []
y_positions = {}

for worker in range(1, 6):
    worker_orders = batch_assignments[batch_assignments['WorkerNo'] == worker].sort_values('TaskNo')
    if len(worker_orders) == 0:
        continue

    y_pos = len(y_labels)
    y_labels.append(f'工人 {worker}')
    y_positions[worker] = y_pos

    # 模拟该工人的时间线
    current_pos = 1
    current_time = 0

    for _, row in worker_orders.iterrows():
        order = row['OrderNo']
        interval = batch_intervals[order]
        travel, new_pos = compute_order_distance(interval['L'], interval['R'], current_pos)

        # 绘制任务块
        ax.barh(y=y_pos, width=travel, left=current_time,
                color=worker_colors[worker], edgecolor='black', alpha=0.7)
        # 在任务块中间标注订单号（可选，如果太多可不标）
        if travel > 50:  # 只标注足够长的任务
            ax.text(current_time + travel / 2, y_pos, order,
                    ha='center', va='center', fontsize=8)

        current_time += travel
        current_pos = new_pos

ax.set_yticks(range(len(y_labels)))
ax.set_yticklabels(y_labels)
ax.set_xlabel('运动距离（时间）', fontsize=12)
ax.set_ylabel('分拣工', fontsize=12)
ax.set_title(f'图G：批次 {rep_batch} 分拣任务甘特图', fontsize=14)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('图G_甘特图.png', dpi=300, bbox_inches='tight')
plt.show()

# ========== 12. 输出论文填空汇总 ==========
print("\n" + "=" * 60)
print("【论文填空汇总 - 第3问】")
print("=" * 60)
print(f"""
【图E/F 填数】
- 工人1订单数: {worker_order_counts[1]}
- 工人2订单数: {worker_order_counts[2]}
- 工人3订单数: {worker_order_counts[3]}
- 工人4订单数: {worker_order_counts[4]}
- 工人5订单数: {worker_order_counts[5]}

- 工人1运动距离: {worker_total[1]:.0f}
- 工人2运动距离: {worker_total[2]:.0f}
- 工人3运动距离: {worker_total[3]:.0f}
- 工人4运动距离: {worker_total[4]:.0f}
- 工人5运动距离: {worker_total[5]:.0f}

【全局指标】
- 最大完工时间 (makespan): {makespan:.0f}
- 平均运动距离: {mean_dist:.0f}
- 运动距离标准差: {std_dist:.2f}
- 最大/最小比值: {max_min_ratio:.2f}

【图G】
- 代表性批次: {rep_batch}
""")