from Student_demo import Student
student1=Student("方锴铭",18,1001)
student2=Student("潘思雨",18,1111)
students=[student1,student2]
for student in students:
    student.show_info()