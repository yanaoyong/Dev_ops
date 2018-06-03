import requests #导入requests 模块
from bs4 import  BeautifulSoup #导入BeautifulSoup 模块
import sys
type = sys.getfilesystemencoding()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}  #给请求指定一个请求头来模拟chrome浏览器
web_url = 'https://bbs.hupu.com/20415703.html'
r = requests.get(web_url, headers=headers) #像目标url地址发送get请求，返回一个response对象
all_a = BeautifulSoup(r.text, 'lxml').find_all('tr')  #获取网页中的所有tr标签
for a in all_a:
    t=print(a.get_text()) #循环获取文字 
with open("comment.txt", "w", encoding="utf-8") as f:
    for a in all_a:
        f.write(a.get_text())
