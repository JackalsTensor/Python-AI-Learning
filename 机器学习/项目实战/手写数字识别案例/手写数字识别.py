#演示KNN算法识别图片，即：手写数字识别案例
"""
介绍：
    每张图片由28*28像素组成的，即：我们的csv有784个像素点，表示每个像素的颜色
    最终构成图像
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib #保存模型
from collections import Counter
from sklearn.metrics import accuracy_score
from PIL import Image

#1.定义函数，接受用户传入的索引，展示该索引对应的图片
def show_digit(idx):
    #1.读取数据集，获取该数据
    df = pd.read_csv("手写数字识别.csv")
    print(df)   #42000行*785列
    #2.判断传入的索引是否越界
    if idx<0 or idx>len(df):
        print("索引越界")
        return
    #3.说明没有越界，获取该索引对应的数据
    x=df.iloc[:,1:]
    y=df.iloc[:,0]
    #4.查看用户传入的索引对应的图片是几
    print(f'该索引对应的图片是：{y.iloc[idx]}')
    #5.查看下用户传入的索引对应的图片
    print(f'该索引对应的图片是：{x.iloc[idx].shape}')
    # print(f"具体的784个像素点数据是：{x.iloc[idx].values}")
    #6.把(784,)转化成(28,28)
    x=x.iloc[idx].values.reshape(28,28)
    print(x)
    #7.具体的绘制灰度图操作
    plt.imshow(x,cmap="gray")
    plt.axis("off")
    plt.show()

#2.定义函数，训练模型，保存模型
def train_model():
    #1.读取数据集
    df = pd.read_csv("手写数字识别.csv")
    #2.数据的预处理
    x=df.iloc[:,1:]
    y=df.iloc[:,0]
    print(f'x的形状是：{x.shape}')  #42000,784
    print(f'y的形状是：{y.shape}')  #42000,
    print(f'查看所有标签的分布情况:{Counter(y)}')
    #2.1 进行归一化操作
    x=x/255
    print(f'归一化后的数据集x的形状是：{x.shape}')
    #2.2 拆分训练集和测试集
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=23,stratify=y)
    #3.模型训练
    estimator=KNeighborsClassifier(n_neighbors=3)
    estimator.fit(x_train,y_train)
    #4.模型评估
    print(f'训练集的准确率是：{estimator.score(x_test,y_test)}')
    print(f'测试集的准确率是：{accuracy_score(y_test,estimator.predict(x_test))}')
    #5.保存模型
    #参一：模型对象  参二：模型保存的路径
    joblib.dump(estimator,"手写数字识别.pkl")
    print("模型保存成功")

#3.定义函数，测试模型
def use_model():
    # ---------------------- 1. 加载并预处理 demo.png ----------------------
    img = Image.open("demo.png").convert("L")  # 强制灰度
    img = img.resize((28, 28))
    img_arr = np.array(img)

    img_norm = img_arr / 255.0
    img_norm = 1 - img_norm  # ✅ 关键：反转黑白，和 MNIST 一致

    img_flat = img_norm.reshape(1, -1)  # (1,784)

    # ---------------------- 2. 加载模型 ----------------------
    model_path = r"/机器学习/项目实战/手写数字识别数据集\手写数字识别.pkl"
    estimator = joblib.load(model_path)

    # ---------------------- 3. 预测+展示 ----------------------
    y_pred = estimator.predict(img_flat)[0]

    plt.imshow(img_arr, cmap="gray")
    plt.axis("off")
    plt.title(f"demo.png | 预测: {y_pred}")
    plt.show()

    print(f"✅ 预测结果: {y_pred}")
    print(f"✅ 图片形状: {img_arr.shape}")
    print(f"✅ 输入模型形状: {img_flat.shape}")
    print(f"✅ 数值范围: {img_norm.min():.3f} ~ {img_norm.max():.3f}")


#4.测试函数
if __name__ == "__main__":
    # show_digit(23)
    # train_model()
    use_model()