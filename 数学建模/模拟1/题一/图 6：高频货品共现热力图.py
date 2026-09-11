import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 1. 读取数据 ==========
df = pd.read_csv(r"D:\PythonProject1\数学建模\模拟1\附件1：订单信息.csv")

# ========== 2. 统计每个货品出现的次数（在多少订单中出现） ==========
item_freq = df.groupby('ItemNo')['OrderNo'].nunique().sort_values(ascending=False)

# 选择前20个高频货品
top_n = 20
top_items = item_freq.head(top_n).index.tolist()

print("=" * 60)
print(f"【高频货品 TOP {top_n}】")
print("=" * 60)
for i, item in enumerate(top_items, 1):
    print(f"{i}. {item}: 出现在 {item_freq[item]} 个订单中")

# ========== 3. 构建订单-货品矩阵（只针对高频货品） ==========
# 筛选出只包含高频货品的订单记录
df_top = df[df['ItemNo'].isin(top_items)]

# 构建一个字典：订单 -> 该订单包含的高频货品集合
order_top_items = df_top.groupby('OrderNo')['ItemNo'].apply(set).to_dict()

# ========== 4. 计算共现矩阵 ==========
# 初始化共现矩阵
cooc_matrix = pd.DataFrame(0, index=top_items, columns=top_items)

# 遍历每个订单，更新共现计数
for order, items in order_top_items.items():
    items_list = list(items)
    for i in range(len(items_list)):
        for j in range(i + 1, len(items_list)):
            a, b = items_list[i], items_list[j]
            cooc_matrix.loc[a, b] += 1
            cooc_matrix.loc[b, a] += 1

# 对角线设为0（不关心货品与自己的共现）
for item in top_items:
    cooc_matrix.loc[item, item] = 0

# ========== 5. 打印共现矩阵统计 ==========
print("\n" + "=" * 60)
print("【共现矩阵统计】")
print("=" * 60)
print(f"共现矩阵大小: {len(top_items)} x {len(top_items)}")
max_cooc = cooc_matrix.max().max()
print(f"最大共现次数: {max_cooc}")
print(f"平均共现次数: {cooc_matrix.sum().sum() / (len(top_items) * (len(top_items)-1)):.2f}")

# ========== 6. 画热力图 ==========
plt.figure(figsize=(14, 12))

# 使用 seaborn 画热力图
sns.heatmap(cooc_matrix,
            annot=True,           # 显示数字
            fmt='d',              # 整数格式
            cmap='YlOrRd',        # 黄-橙-红渐变色
            linewidths=0.5,
            linecolor='gray',
            square=True,
            cbar_kws={'label': '共现次数'})

plt.title(f'高频货品共现热力图 (TOP {top_n})', fontsize=16)
plt.xlabel('货品编号', fontsize=12)
plt.ylabel('货品编号', fontsize=12)

# 旋转x轴标签，避免重叠
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

plt.tight_layout()
plt.savefig('图X_高频货品共现热力图.png', dpi=300, bbox_inches='tight')
plt.show()

# ========== 7. 输出强关联货品对（用于第2问分析） ==========
print("\n" + "=" * 60)
print("【强关联货品对（共现次数最高的10对）】")
print("=" * 60)

# 获取上三角矩阵的索引和值
pairs = []
for i in range(len(top_items)):
    for j in range(i + 1, len(top_items)):
        if cooc_matrix.iloc[i, j] > 0:
            pairs.append({
                'item1': top_items[i],
                'item2': top_items[j],
                'cooc': cooc_matrix.iloc[i, j]
            })

# 按共现次数排序
pairs_sorted = sorted(pairs, key=lambda x: x['cooc'], reverse=True)

# 输出前10对
for i, pair in enumerate(pairs_sorted[:10], 1):
    print(f"{i}. {pair['item1']} & {pair['item2']}: 共现 {pair['cooc']} 次")

print("\n" + "=" * 60)
print("【论文描述模板（可直接使用）】")
print("=" * 60)
print(f"""
图X展示了出现频率最高的{top_n}个货品之间的共现热力图。其中，颜色越深表示两货品在同一订单中共同出现的次数越多。

从图中可以看出：
- 最大共现次数为 {max_cooc} 次
- 强关联货品对包括：{pairs_sorted[0]['item1']}与{pairs_sorted[0]['item2']}（共现{pairs_sorted[0]['cooc']}次）、{pairs_sorted[1]['item1']}与{pairs_sorted[1]['item2']}（共现{pairs_sorted[1]['cooc']}次）等。

这些强关联货品应在第2问的货架摆放中尽量靠近，以缩短订单的拣选距离。
""")