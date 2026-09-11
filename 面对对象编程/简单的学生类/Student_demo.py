class Student():
    def __init__(self,name,age,student_id):
        self.name = name
        self.age = age
        self.student_id = student_id
    def show_info(self):
        print(f"这个人名字是{self.name},年龄为{self.age},ID号为{self.student_id}")
