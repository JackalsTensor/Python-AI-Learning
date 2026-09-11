import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ========== 1. 中文乱码修复 ==========
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ========== 2. 已知参数 ==========
days_since_winter_solstice = 44
epsilon_deg = 23.65554  # 黄赤交角
epsilon_rad = np.radians(epsilon_deg)

# 计算黄经λ（冬至黄经270°）
lambda_deg = 270 + days_since_winter_solstice / 365.24219 * 360
lambda_rad = np.radians(lambda_deg)
beta_deg = 0  # 黄纬为0（太阳在黄道上）
beta_rad = np.radians(beta_deg)

# ========== 3. 黄赤道坐标转换公式 ==========
cos_delta_cos_alpha = np.cos(beta_rad) * np.cos(lambda_rad)
cos_delta_sin_alpha = np.cos(epsilon_rad) * np.cos(beta_rad) * np.sin(lambda_rad) - np.sin(epsilon_rad) * np.sin(beta_rad)
sin_delta = np.sin(epsilon_rad) * np.cos(beta_rad) * np.sin(lambda_rad) + np.cos(epsilon_rad) * np.sin(beta_rad)

# 求解赤经α、赤纬δ
delta_rad = np.arcsin(sin_delta)
alpha_rad = np.arctan2(cos_delta_sin_alpha, cos_delta_cos_alpha)
# 转成角度
delta_deg = np.degrees(delta_rad)
alpha_deg = np.degrees(alpha_rad)
if alpha_deg < 0:
    alpha_deg += 360

print(f"冬至后{days_since_winter_solstice}日：")
print(f"黄经λ = {lambda_deg:.4f}°")
print(f"赤经α = {alpha_deg:.4f}°")
print(f"赤纬δ = {delta_deg:.4f}°")

# ========== 4. 天球模型 ==========
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制天球网格（单位球）
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color='lightgray', alpha=0.3)

# 赤道（z=0的大圆）
theta = np.linspace(0, 2*np.pi, 100)
eq_x = np.cos(theta)
eq_y = np.sin(theta)
eq_z = np.zeros_like(theta)
ax.plot(eq_x, eq_y, eq_z, color='red', linewidth=2, label='赤道')

# 黄道（绕X轴旋转黄赤交角）
ecl_x = np.cos(theta)
ecl_y = np.cos(epsilon_rad)*np.sin(theta)
ecl_z = np.sin(epsilon_rad)*np.sin(theta)
ax.plot(ecl_x, ecl_y, ecl_z, color='gold', linewidth=2, label='黄道')

# 太阳位置（转成三维坐标）
sun_x = np.cos(delta_rad) * np.cos(alpha_rad)
sun_y = np.cos(delta_rad) * np.sin(alpha_rad)
sun_z = np.sin(delta_rad)
ax.scatter(sun_x, sun_y, sun_z, color='purple', s=150, label='太阳位置')
ax.text(sun_x+0.05, sun_y+0.05, sun_z+0.05, "太阳", fontsize=12, weight='bold')

# 标注二分二至点
solstices = [
    (270, 0, "冬至", "blue"),
    (0, 0, "春分", "green"),
    (90, 0, "夏至", "red"),
    (180, 0, "秋分", "brown")
]
for lam_deg, bet_deg, name, color in solstices:
    lam_r = np.radians(lam_deg)
    bet_r = np.radians(bet_deg)
    # 转赤道坐标
    cdc = np.cos(bet_r) * np.cos(lam_r)
    cds = np.cos(epsilon_rad) * np.cos(bet_r) * np.sin(lam_r) - np.sin(epsilon_rad) * np.sin(bet_r)
    sd = np.sin(epsilon_rad) * np.cos(bet_r) * np.sin(lam_r) + np.cos(epsilon_rad) * np.sin(bet_r)
    d_r = np.arcsin(sd)
    a_r = np.arctan2(cds, cdc)
    sx = np.cos(d_r) * np.cos(a_r)
    sy = np.cos(d_r) * np.sin(a_r)
    sz = np.sin(d_r)
    ax.scatter(sx, sy, sz, color=color, s=100)
    ax.text(sx+0.05, sy+0.05, sz+0.05, name, fontsize=12, color=color, weight='bold')

# ========== 5. 坐标轴 ==========
ax.set_xlabel('X', fontsize=14)
ax.set_ylabel('Y', fontsize=14)
ax.set_zlabel('Z', fontsize=14)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_zlim(-1.2, 1.2)
ax.view_init(elev=25, azim=-45)
plt.title('黄赤道坐标转换 - 太阳位置可视化', fontsize=18, weight='bold', pad=20)
ax.legend()

plt.tight_layout()
plt.show()