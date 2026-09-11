import pyautogui
import pyperclip
import time

# ================= 自定义参数（按需修改）=================
message = ("")  # 要发送的消息
send_count = 99 # 发送次数（避免无限刷屏，建议设有限次数）
interval = 0.0000001

# 预留5秒准备时间：运行脚本后，快速切换到聊天窗口并点击输入框
print(f"5秒后开始刷屏，共发送{send_count}条消息...")
time.sleep(5)

for i in range(send_count):
    # 1. 将消息复制到剪贴板
    pyperclip.copy(message)
    # 2. 模拟键盘操作：Ctrl+V粘贴，Enter发送
    pyautogui.hotkey("ctrl", "v")  # 粘贴消息
    pyautogui.press("enter")       # 发送消息
    # 3. 间隔一段时间，避免发送过快被风控
    time.sleep(interval)

print("刷屏完成！")