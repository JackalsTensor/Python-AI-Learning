class BankAccount:
    def __init__(self):
        self.__balance = 0
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"存款成功,存入{amount}元，当前余额:{self.__balance}元")
        else:
            print("存款失败")
    def withdraw(self, amount):
        if amount <= 0:
            print("存款失败")
        elif amount > self.__balance:
            print(f"取款失败！")
        else:
            self.__balance -= amount
            print(f"取款成功！当前余额为{self.__balance}元，不足以取出{amount}元。")
    def get_balance(self):
        print(f"当前余额为{self.__balance}")