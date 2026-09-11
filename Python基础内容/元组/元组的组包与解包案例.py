#交换两个变量值
a=10
b=20

#组包
t=b,a
#解包
a,b=t

print(a)
print(b)


#对三个变量值进行交换
a=100
b=200
c=300

c,a,b=a,b,c
print(a)
print(b)
print(c)