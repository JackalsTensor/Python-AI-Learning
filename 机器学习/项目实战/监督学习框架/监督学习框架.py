''''
# 1. 导入需要的库（工具包）
import 数据集库          # 如 sklearn.datasets
import 数据拆分库        # 如 sklearn.model_selection.train_test_split
import 数据预处理库      # 如 sklearn.preprocessing.StandardScaler
import 模型库            # 如 sklearn.neighbors.KNeighborsClassifier
import 评估库            # 如 sklearn.metrics.accuracy_score（可选）

# 2. 加载/准备数据（有监督学习必须有“特征x”和“标签y”）
数据集 = 加载数据集()    # 如 load_wine()
x = 数据集.data          # 所有样本的特征（输入）
y = 数据集.target        # 所有样本的标签（输出，比如类别0/1/2）

# 3. 拆分训练集/测试集（用训练集学，测试集考）
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42  # test_size=测试集比例，random_state=固定拆分方式
)

# 4. 数据预处理（标准化/归一化等，让模型学得更好）
预处理工具 = 预处理方法()                  # 如 StandardScaler()
x_train = 预处理工具.fit_transform(x_train)# 用训练集“学”预处理规则，再转换
x_test = 预处理工具.transform(x_test)      # 测试集直接用训练集的规则（不重新学）

# 5. 定义模型 + 训练模型 + 预测
模型 = 选择的模型(超参数)                  # 如 KNeighborsClassifier(n_neighbors=3)
模型.fit(x_train, y_train)                 # 用训练集“教”模型
y_test_pred = 模型.predict(x_test)         # 用测试集“考”模型，得到预测结果
新样本_pred = 模型.predict(新样本预处理后)  # （可选）预测新数据

# 6. 模型评估（看模型考得怎么样，可选但重要）
准确率 = 评估指标(y_test, y_test_pred)    # 如 accuracy_score(y_test, y_test_pred)
print(f"模型准确率：{准确率:.2f}")          # 比如输出“模型准确率：0.97”（97分）
'''''