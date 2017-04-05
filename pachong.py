import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'http://www.mzitu.com'  ##开始的URL地址
start_html = requests.get(all_url,  headers=headers)  
##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
#print(start_html.text) 
##打印出start_html (请注意，concent是二进制的数据，一般用于下载图片、视频、音频、等多媒体内容是才使用concent, 对于打印网页内容请使用text)
Soup = BeautifulSoup(start_html.text, 'lxml')
#li_list=Soup.find_all('li')
#for li in li_list:
#	print(li)
all_a = Soup.find('ul', id ='pins').find_all('a') ##意思是先查找id为 pins 的ul标签，然后查找所有的<a>标签。
a1 = all_a[1::2]
#print(all_a)
#print(a1)
for a in a1:
    title = a.get_text() #取出a标签的文本
    #print(title)
    #print(a)
    path = str(title).strip() ##去掉空格
    #print(path)
    os.makedirs(os.path.join("D:\mzitu", path)) ##创建一个存放套图的文件夹
    #os.chdir("D:\mzitu\\"+path) ##切换到上面创建的文件夹
    href = a['href']
    #print(href)
    html = requests.get(href, headers=headers)
    html_Soup = BeautifulSoup(html.text, 'lxml')
    max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
    #print(max_span)
    for page in range(1, int(max_span)+1): ##不知道为什么这么用的小哥儿去看看基础教程吧
        page_url = href + '/' + str(page) ##同上
        #print(page_url) ##这个page_url就是每张图片的页面地址啦！但还不是实际地址！
        img_html = requests.get(page_url, headers=headers)
        img_Soup = BeautifulSoup(img_html.text, 'lxml')
        img_url = img_Soup.find('div', class_='main-image').find('img')['src'] ##这三行上面都说过啦不解释了哦
        #print(img_url)
        img = requests.get(img_url, headers=headers)
        name = img_url[-9:-4]
        f = open(name+'.jpg','ab')
        f.write(img.content)
        f.close()

    