import requests
from bs4 import BeautifulSoup
headers = {
    "user-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.8151 SLBChan/115 SLBVPV/64-bit"
}
for start_num in range(0,250,25):
    print(start_num)
    response=requests.get(f"https://movie.douban.com/top250?start={start_num}",headers=headers)
    html=response.text
    soup=BeautifulSoup(html,"html.parser")
    all_titles=soup.findAll("span",attrs={"class":"title"})
    for title in all_titles:
        title_string=(title.string)
        if "/" not in title_string:
            print(title_string)