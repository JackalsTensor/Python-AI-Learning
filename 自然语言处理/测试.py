import numpy as np
import matplotlib.pyplot as plt

# 生成一个正弦波信号
sampling_rate = 1000  # 采样率
T = 1.0 / sampling_rate  # 采样周期
t = np.arange(0.0, 1.0, T)  # 时间向量，持续1秒
f = 5.0  # 信号频率 5 Hz
signal = np.sin(2 * np.pi * f * t)  # 生成正弦波信号

# 绘制原始信号
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.title("原始信号 (正弦波)")
plt.xlabel("时间 [s]")
plt.ylabel("幅度")

# 进行傅里叶变换
fourier_transform = np.fft.fft(signal)  # 计算傅里叶变换
frequencies = np.fft.fftfreq(len(t), T)  # 频率轴

# 绘制傅里叶变换的幅度谱（频域图）
plt.subplot(2, 1, 2)
plt.plot(frequencies[:len(frequencies)//2], np.abs(fourier_transform)[:len(frequencies)//2])  # 仅绘制正频率部分
plt.title("傅里叶变换的幅度谱")
plt.xlabel("频率 [Hz]")
plt.ylabel("幅度")
plt.tight_layout()
plt.show()

# 重建信号：通过逆傅里叶变换
reconstructed_signal = np.fft.ifft(fourier_transform)

# 绘制重建后的信号
plt.figure(figsize=(8, 4))
plt.plot(t, reconstructed_signal.real)
plt.title("通过傅里叶变换重建的信号")
plt.xlabel("时间 [s]")
plt.ylabel("幅度")
plt.show()