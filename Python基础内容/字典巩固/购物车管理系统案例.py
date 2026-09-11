"""
案例:
开发一个购物车管理系统，实现商品信息的添加、修改、删除、查询和统计功能。系统使用嵌套字典结构存储商品数据，通过控制台菜单与用户交互。
具体功能如下:
1．添加购物车: 用户根据提示录入商品名称、以及该商品的价格、数量，保存该商品信息到购物车。
2．修改购物车: 要求用户输入要修改的购物车商品名称，然后再提示输入该商品的价格、数量，输入完成后修改该商品信息。
3．删除购物车: 要求用户输入要删除的购物车名称，根据名称删除购物车中的商品。
4．查询购物车: 将购物车中的商品信息展示出来，格式为: "商品名称: xxx，商品价格: xxx，商品数量: xxx"。
5．退出购物车
"""

shopping_cart = {}

while True:
    # 1.制作菜单
    print("欢迎使用购物车管理系统")
    menu = """
########购物车管理系统########
       1. 添加购物车
       2. 修改购物车
       3. 删除购物车
       4. 查询购物车
       5. 退出购物车
###########################
    """
    print(menu)

    # 2.执行的具体操作
    choice = input("请选择需要执行的操作: ")
    match choice:
        case "1":  # 添加购物车
            goods_name = input("请输入商品名称: ")
            goods_price = float(input("请输入商品价格: "))
            goods_num = int(input("请输入商品数量: "))
            # 先判断是否存在
            if goods_name in shopping_cart:
                print("该商品已在购物车中，无法重复添加。")
            else:
                shopping_cart[goods_name] = {"price": goods_price, "num": goods_num}
                print("商品添加完毕")

        case "2":  # 修改购物车 
            goods_name = input("请输入要修改的商品名称: ")
            if goods_name not in shopping_cart:
                print("该商品不存在，请重新选择。")
            else:
                goods_price = float(input("请输入新商品价格: "))
                goods_num = int(input("请输入新商品数量: "))
                shopping_cart[goods_name]["price"] = goods_price
                shopping_cart[goods_name]["num"] = goods_num
                print("商品修改完毕")

        case "3":  # 删除购物车
            goods_name = input("请输入要删除的商品名称: ")
            if goods_name not in shopping_cart:
                print("该商品不存在，请重新选择。")
            else:
                del shopping_cart[goods_name]
                print("商品删除完毕")

        case "4":  # 查询购物车
            if len(shopping_cart) == 0:
                print("购物车暂无商品！")
            else:
                for goods_name in shopping_cart.keys():
                    goods_info = shopping_cart[goods_name]
                    print(f"商品名称: {goods_name}，商品价格: {goods_info['price']}，商品数量: {goods_info['num']}")

        case "5":  # 退出购物车
            print("已退出购物车系统")
            break

        case _:
            print("无效的选择，请重新输入。")
    print("-" * 30)