import urllib.request
#下载网页
url_page='http://www.baidu.com/'
#url代表的是下载路径，filename啊代表文件名字
urllib.request.urlretrieve(url_page,'baidu.html')
#下载图片
url_img='https://tse4-mm.cn.bing.net/th/id/OIP-C.HXkuhtU0zZTsr9ces3j59wHaHD?w=186&h=180&c=7&r=0&o=7&dpr=1.5&pid=1.7&rm=3.jpg'
urllib.request.urlretrieve(url=url_img, filename='../AI应用开发/资源/img.jpg')
#下载视频
# url_video='<script src="https://mediago-static.cdn.bcebos.com/haokan/bundle-3.2.1.js">'