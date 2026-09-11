#获取百度页面源码
import urllib.request
url='https://www.baidu.com/'
#模仿浏览器对页面发送请求
response=urllib.request.urlopen(url)
#获取响应中页面源码
content=response.read().decode('utf-8')
print(content)