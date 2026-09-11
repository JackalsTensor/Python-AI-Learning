import tkinter as tk
import random
import time

bless_core = [
    "记得好好护肤", "梦想成真", "顺顺利利", "你超棒的",
    "多喝水哦~", "今天过得开心嘛", "好好爱自己", "保持微笑呀",
    "期待下一次见面", "别熬夜哦", "要天天开心", "暴富暴美",
    "事事顺遂", "平安喜乐", "万事胜意", "光芒万丈",
    "好运连连", "福气满满", "心想事成", "一路繁花",
    "学业进步", "工作顺利", "身体健康", "天天开心"
]

bg_colors = [
    "#FFE4E1", "#F0E6FA", "#FFF0F5", "#E0FFFF", "#FAF0E6", "#F5F5DC",
    "#DDA0DD", "#ADD8E6", "#F0FFF0", "#FFEBCD", "#FFDAB9", "#E6E6FA"
]


def create_bless_window():
    top = tk.Toplevel()
    top.overrideredirect(True)
    top.attributes("-topmost", True)

    core = random.choice(bless_core)
    bless = f"xxx{core}"
    bg_color = random.choice(bg_colors)

    icon_label = tk.Label(top, text="💖 提示", bg=bg_color, font=("微软雅黑", 12, "bold"))
    icon_label.pack(side=tk.LEFT, padx=8)

    text_label = tk.Label(top, text=bless, bg=bg_color, font=("微软雅黑", 14))
    text_label.pack(side=tk.LEFT, padx=8, pady=15)

    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    x = random.randint(50, screen_width - 250)
    y = random.randint(50, screen_height - 100)
    top.geometry(f"250x70+{x}+{y}")

    top.after(10000, top.destroy)


root = tk.Tk()
root.withdraw()

# 间隔改为0.1秒，100个窗口约10秒内弹完
for _ in range(300):
    create_bless_window()
    time.sleep(0.01)

root.mainloop()