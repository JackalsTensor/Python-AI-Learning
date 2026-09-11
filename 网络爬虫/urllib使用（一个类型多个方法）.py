import urllib.request
url='http://www.baidu.com'
response=urllib.request.urlopen(url)
#一个类型和六个方法
# response是HTTPResponse的类型
# print(type(response))

# #返回多少个字节
# content=response.read(5).decode('utf-8')
# print(content)

# #读取一行
# content=response.readline()
# print(content)

# content=response.readlines()
# print(content)

#返回状态码
print(response.getcode())

#返回url地址
print(response.geturl())

#获取的是一些状态信息
print(response.getheaders())