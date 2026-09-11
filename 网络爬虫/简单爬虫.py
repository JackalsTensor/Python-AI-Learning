import requests
headers = {
    "authority": "www.hnnu.edu.cn",
    "method": "GET",
    "path": "/",
    "scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Cookie": "JSESSIONID=96867933213B517BF72AECB9968CF48; u=0,1",
    "Priority": "u=0,i",
    "Referer": "https://www.baidu.com/link?url=I5l4VAyA9f7sUswzAjmk3r1T8G0UalEnPnNkyY2cw21VS22IkodW9CN5nxl&wd=&eqid=da54ae0300919a3e0000000569286298",
    "Sec-Ch-Ua": "\"Chromium\";v=\"9\", \"Not_A Brand\";v=\"8\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.8151 SLBChat/115 SLBPV/64-bit"
}
url="https://www.hnnu.edu.cn"
response = requests.get(url,headers=headers)
response.encoding=response.apparent_encoding
print("响应状态码:",response.status_code)
print("响应内容:",response.text)
