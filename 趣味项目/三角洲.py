import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# =========================
# 🧿 1. 数据集（可扩展）
# =========================
data = [
    ("事业发展顺利前景光明", "乾卦"),
    ("领导能力强适合决策", "乾卦"),
    ("稳定守成不宜冒进", "坤卦"),
    ("包容承载厚德载物", "坤卦"),
    ("变化多端不确定因素多", "巽卦"),
    ("风向变化注意调整策略", "巽卦"),
    ("情绪波动起伏明显", "震卦"),
    ("突发事件需要快速反应", "震卦"),
    ("沟通顺畅人际关系良好", "兑卦"),
    ("喜悦交流合作顺利", "兑卦"),
    ("困难阻碍需要谨慎", "坎卦"),
    ("风险较高注意安全", "坎卦"),
    ("光明上升积极发展", "离卦"),
    ("目标明确前进方向清晰", "离卦"),
    ("艰难阻滞需要坚持", "艮卦"),
    ("停止调整不宜行动", "艮卦"),
]

df = pd.DataFrame(data, columns=["text", "label"])

# =========================
# 🧠 2. 机器学习模型
# =========================
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000))
])

X = df["text"]
y = df["label"]

model.fit(X, y)

# =========================
# 🧿 3. 八卦解释系统
# =========================
bagua_meaning = {
    "乾卦": "☰ 天行健，君子以自强不息（主动、进取）",
    "坤卦": "☷ 地势坤，厚德载物（包容、稳定）",
    "震卦": "☳ 雷动，变动与行动（突发、变化）",
    "巽卦": "☴ 风，渗透与变化（灵活、适应）",
    "坎卦": "☵ 水，险中求进（风险、挑战）",
    "离卦": "☲ 火，光明与方向（清晰、成长）",
    "艮卦": "☶ 山，止与稳定（停止、沉淀）",
    "兑卦": "☱ 泽，喜悦与交流（沟通、人际）",
}

# =========================
# 🧠 4. 预测函数
# =========================
def predict_bagua(text):
    pred = model.predict([text])[0]
    return pred, bagua_meaning.get(pred, "未知卦象")

# =========================
# 🖥️ 5. 交互系统
# =========================
print("\n🧠 AI道教机器学习系统 v1")
print("输入问题（输入 exit 退出）\n")

while True:
    user = input("👉 请输入：")

    if user == "exit":
        break

    label, meaning = predict_bagua(user)

    print("\n🧿 卦象预测：", label)
    print("📖 解读：", meaning)
    print("-" * 50)