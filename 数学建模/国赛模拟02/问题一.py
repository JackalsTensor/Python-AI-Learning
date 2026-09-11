import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 已知参数
g = 9.8  # 重力加速度

# 初始位置
FY1_start = np.array([17800, 0, 1800])
M1_start = np.array([20000, 0, 2000])
target = np.array([0, 0, 0])  # 假目标

# 时间参数
t_drop = 1.5  # 投放时间
t_detonate = 5.1  # 起爆时间
t_end = 30  # 模拟结束时间

# 无人机参数
v_FY1 = 120  # 速度
dir_FY1 = -FY1_start / np.linalg.norm(FY1_start)  # 朝向原点的方向

# 导弹参数
v_M1 = 300
dir_M1 = -M1_start / np.linalg.norm(M1_start)

print("=" * 60)
print("问题1：烟幕干扰弹对M1的有效遮蔽时长分析")
print("=" * 60)

# 计算投放点
P_drop = FY1_start + v_FY1 * t_drop * dir_FY1
print(f"\n1. 投放点位置 (t={t_drop}s):")
print(f"   x = {P_drop[0]:.2f} m")
print(f"   y = {P_drop[1]:.2f} m")
print(f"   z = {P_drop[2]:.2f} m")

# 烟幕弹初始速度（与无人机相同）
v_smoke = v_FY1 * dir_FY1

# 计算起爆点
dt = t_detonate - t_drop
P_detonate = P_drop.copy()
P_detonate[0] += v_smoke[0] * dt
P_detonate[2] = P_drop[2] + v_smoke[2] * dt - 0.5 * g * dt ** 2

print(f"\n2. 起爆点位置 (t={t_detonate}s):")
print(f"   x = {P_detonate[0]:.2f} m")
print(f"   y = {P_detonate[1]:.2f} m")
print(f"   z = {P_detonate[2]:.2f} m")

# 生成时间序列
t = np.linspace(0, t_end, 1000)

# 无人机轨迹（仅到投放点）
FY1_traj = np.zeros((len(t), 3))
for i, ti in enumerate(t):
    if ti <= t_drop:
        FY1_traj[i] = FY1_start + v_FY1 * ti * dir_FY1
    else:
        FY1_traj[i] = P_drop  # 投放后无人机继续飞行，但这里简化处理

# 烟幕弹轨迹（投放后到起爆）
smoke_traj = np.zeros((len(t), 3))
for i, ti in enumerate(t):
    if ti < t_drop:
        smoke_traj[i] = FY1_traj[i]  # 还在无人机上
    elif ti <= t_detonate:
        t_smoke = ti - t_drop
        smoke_traj[i] = P_drop.copy()
        smoke_traj[i, 0] += v_smoke[0] * t_smoke
        smoke_traj[i, 2] = P_drop[2] + v_smoke[2] * t_smoke - 0.5 * g * t_smoke ** 2
    else:
        smoke_traj[i] = P_detonate  # 起爆后位置固定（水平）

# 烟幕中心下沉轨迹（起爆后）
smoke_center_traj = np.zeros((len(t), 3))
for i, ti in enumerate(t):
    if ti < t_detonate:
        smoke_center_traj[i] = smoke_traj[i]
    else:
        smoke_center_traj[i] = P_detonate.copy()
        smoke_center_traj[i, 2] = P_detonate[2] - 3 * (ti - t_detonate)

# 导弹轨迹
M1_traj = np.zeros((len(t), 3))
for i, ti in enumerate(t):
    M1_traj[i] = M1_start + v_M1 * ti * dir_M1

# 计算距离
distances = []
valid_times = []

print(f"\n3. 遮蔽效果分析:")
print(f"   烟幕有效时间窗口: {t_detonate}s - {t_detonate + 20}s")

# 检查每个时刻的距离
for i, ti in enumerate(t):
    if t_detonate <= ti <= t_detonate + 20:
        # 导弹位置
        M1_pos = M1_traj[i]
        # 烟幕中心位置
        smoke_pos = smoke_center_traj[i]

        # 计算距离
        dist = np.sqrt(np.sum((M1_pos - smoke_pos) ** 2))
        distances.append(dist)
        valid_times.append(ti)

        if dist <= 10:
            print(f"   t={ti:.2f}s: 距离={dist:.2f}m ✅ 有效遮蔽")
        else:
            if ti == t_detonate:
                print(f"   t={ti:.2f}s: 距离={dist:.2f}m ❌ 无效")
            elif abs(ti - t_detonate - 10) < 0.1:
                print(f"   t={ti:.2f}s: 距离={dist:.2f}m ❌ 无效")
            elif abs(ti - t_detonate + 20) < 0.1:
                pass  # 最后一个点不重复打印

# 检查最小距离
min_dist = min(distances) if distances else float('inf')
min_time = valid_times[np.argmin(distances)] if distances else 0

print(f"\n4. 结果汇总:")
print(f"   最小距离: {min_dist:.2f} m (发生在 t={min_time:.2f}s)")
print(f"   有效遮蔽时长: 0 s (最小距离 {min_dist:.2f}m > 10m)")

if min_dist > 10:
    print(f"\n✅ 结论: 烟幕弹完全无法遮蔽M1导弹")
else:
    print(f"\n❌ 结论: 存在有效遮蔽窗口")

# ==================== 可视化部分 ====================
fig = plt.figure(figsize=(16, 10))

# 3D轨迹图
ax1 = fig.add_subplot(221, projection='3d')
ax1.plot(FY1_traj[:int(t_drop * len(t) / t_end), 0],
         FY1_traj[:int(t_drop * len(t) / t_end), 1],
         FY1_traj[:int(t_drop * len(t) / t_end), 2],
         'b-', label='无人机轨迹', linewidth=2)
ax1.plot(smoke_traj[int(t_drop * len(t) / t_end):int(t_detonate * len(t) / t_end), 0],
         smoke_traj[int(t_drop * len(t) / t_end):int(t_detonate * len(t) / t_end), 1],
         smoke_traj[int(t_drop * len(t) / t_end):int(t_detonate * len(t) / t_end), 2],
         'g--', label='烟幕弹轨迹', linewidth=2)
ax1.plot(M1_traj[:, 0], M1_traj[:, 1], M1_traj[:, 2],
         'r-', label='导弹轨迹', linewidth=2)

# 标记关键点
ax1.scatter(*FY1_start, c='b', s=100, marker='o', label='FY1起始点')
ax1.scatter(*M1_start, c='r', s=100, marker='^', label='M1起始点')
ax1.scatter(*P_drop, c='g', s=150, marker='*', label='投放点')
ax1.scatter(*P_detonate, c='orange', s=200, marker='*', label='起爆点')
ax1.scatter(*target, c='k', s=200, marker='s', label='假目标')

# 绘制烟幕有效范围（起爆后）
theta = np.linspace(0, 2 * np.pi, 20)
for ti in [t_detonate, t_detonate + 10, t_detonate + 20]:
    if ti <= t_end:
        x = P_detonate[0] + 10 * np.cos(theta)
        y = P_detonate[1] + 10 * np.sin(theta)
        z = (P_detonate[2] - 3 * (ti - t_detonate)) * np.ones_like(theta)
        ax1.plot(x, y, z, 'orange', alpha=0.3, linewidth=1)

ax1.set_xlabel('X (m)')
ax1.set_ylabel('Y (m)')
ax1.set_zlabel('Z (m)')
ax1.set_title('3D轨迹图')
ax1.legend()
ax1.view_init(elev=20, azim=-30)

# X-Z平面投影
ax2 = fig.add_subplot(222)
ax2.plot(FY1_traj[:int(t_drop * len(t) / t_end), 0],
         FY1_traj[:int(t_drop * len(t) / t_end), 2],
         'b-', label='无人机轨迹', linewidth=2)
ax2.plot(smoke_traj[int(t_drop * len(t) / t_end):int(t_detonate * len(t) / t_end), 0],
         smoke_traj[int(t_drop * len(t) / t_end):int(t_detonate * len(t) / t_end), 2],
         'g--', label='烟幕弹轨迹', linewidth=2)
ax2.plot(M1_traj[:, 0], M1_traj[:, 2], 'r-', label='导弹轨迹', linewidth=2)

# 标记关键点
ax2.scatter(*FY1_start[[0, 2]], c='b', s=100, marker='o')
ax2.scatter(*M1_start[[0, 2]], c='r', s=100, marker='^')
ax2.scatter(*P_drop[[0, 2]], c='g', s=150, marker='*')
ax2.scatter(*P_detonate[[0, 2]], c='orange', s=200, marker='*')
ax2.scatter(*target[[0, 2]], c='k', s=200, marker='s')

# 绘制烟幕有效范围
for ti in [t_detonate, t_detonate + 10, t_detonate + 20]:
    if ti <= t_end:
        z_smoke = P_detonate[2] - 3 * (ti - t_detonate)
        circle = plt.Circle((P_detonate[0], z_smoke), 10,
                            fill=False, color='orange', alpha=0.5)
        ax2.add_patch(circle)

ax2.set_xlabel('X (m)')
ax2.set_ylabel('Z (m)')
ax2.set_title('X-Z平面投影')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.axis('equal')

# 距离-时间图
ax3 = fig.add_subplot(223)
ax3.plot(valid_times, distances, 'b-', linewidth=2, label='导弹-烟幕中心距离')
ax3.axhline(y=10, color='r', linestyle='--', linewidth=2, label='有效阈值(10m)')
ax3.axvline(x=t_detonate, color='g', linestyle=':', linewidth=1, label='起爆时刻')
ax3.axvline(x=t_detonate + 20, color='g', linestyle=':', linewidth=1, label='有效结束时刻')

# 填充有效区域
y_fill = np.array([0, 50])
x_fill = np.array([t_detonate, t_detonate + 20])
ax3.fill_betweenx(y_fill, x_fill[0], x_fill[1], alpha=0.2, color='green', label='有效时间窗口')

ax3.set_xlabel('时间 (s)')
ax3.set_ylabel('距离 (m)')
ax3.set_title('导弹与烟幕中心距离随时间变化')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.set_ylim([0, max(distances) * 1.1])

# 高度-时间图
ax4 = fig.add_subplot(224)
ax4.plot(t, M1_traj[:, 2], 'r-', linewidth=2, label='导弹高度')
ax4.plot(t, smoke_center_traj[:, 2], 'b-', linewidth=2, label='烟幕中心高度')
ax4.axhline(y=P_detonate[2], color='orange', linestyle=':', linewidth=1, label='起爆高度')
ax4.axvline(x=t_drop, color='purple', linestyle=':', linewidth=1, label='投放时刻')
ax4.axvline(x=t_detonate, color='g', linestyle=':', linewidth=1, label='起爆时刻')

ax4.set_xlabel('时间 (s)')
ax4.set_ylabel('高度 (m)')
ax4.set_title('高度随时间变化')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.suptitle('问题1：烟幕干扰弹投放效果分析', fontsize=16, y=1.02)
plt.show()

# 打印详细的时间序列数据
print("\n" + "=" * 60)
print("5. 详细时间序列数据（每2秒）")
print("=" * 60)
print(f"{'时间(s)':<10} {'导弹X(m)':<15} {'导弹Z(m)':<15} {'烟幕X(m)':<15} {'烟幕Z(m)':<15} {'距离(m)':<15}")
print("-" * 85)

for ti in np.arange(0, t_end + 1, 2):
    idx = int(ti * len(t) / t_end)
    if idx < len(t):
        M1_pos = M1_traj[idx]
        smoke_pos = smoke_center_traj[idx]
        dist = np.sqrt(np.sum((M1_pos - smoke_pos) ** 2))

        # 判断是否在有效时间窗口内
        if t_detonate <= ti <= t_detonate + 20:
            status = "✅" if dist <= 10 else "❌"
        else:
            status = " "

        print(f"{ti:<10.1f} {M1_pos[0]:<15.1f} {M1_pos[2]:<15.1f} "
              f"{smoke_pos[0]:<15.1f} {smoke_pos[2]:<15.1f} {dist:<15.2f} {status}")

