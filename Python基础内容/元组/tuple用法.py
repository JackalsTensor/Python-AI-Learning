#元组tuple的组包和解包操作
#组包操作
t1=(5,7,9,10,2,23,12)

t2=5,7,9,10,2,23,12

print(t1)
print(t2)

#解包操作
#基础解包(变量数量和容器元素数量一模一样)
a,b,c,d,e,f,g=t1
print(a,b,c,d,e,f,g)

first,second,*other,last=t1
print(first,second)
print(other)
print(last)