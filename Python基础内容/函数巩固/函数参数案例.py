# -------------------- 函数 - 默认参数 --------------------
# 定义函数
def reg_stu(name, age, gender="男", city="北京"):
    print(f"注册成功，姓名: {name}, 年龄: {age}, 性别: {gender}, 城市: {city}")
    return {"name": name, "age": age, "gender": gender, "city": city}

# 调用函数
stu = reg_stu(name="王林", age=20)
print(stu)

stu = reg_stu(name="李慕婉", age=18, gender="女")
print(stu)

stu = reg_stu(name="韩立", age=22, city="上海")
print(stu)

# -------------------- 函数 - 不定长参数(位置参数 *args --> 元组) --------------------
# 需求：根据传入的这批数据，计算这批数据的最小值，最大值，平均值
def calc_data(*args):
    min_data = min(args)
    max_data = max(args)
    avg_data = sum(args) / len(args)
    return min_data, max_data, round(avg_data, 1)

# 调用函数
print(calc_data(2, 7, 9, 10, 45))
print(calc_data(2, 7, 9, 10, 45, 73, 37, 93, 92, 111, 222))