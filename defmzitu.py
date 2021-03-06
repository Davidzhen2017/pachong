
import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os,sys,io,datetime
from Download import request
import mysql.connector

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'http://www.mzitu.com'  ##开始的URL地址
start_html = requests.get(all_url,  headers=headers)  

class mzitu():
	def __init__(self):
		#conn = mysql.connector.connect(user='root', password='123456', database='test')
		#cursor = conn.cursor()
		# 创建pachong表:
		#cursor.execute('create table pachong (id varchar(20) primary key, name varchar(20), addr varchar(20), time varchar(20))')
		#cursor.close()
		#conn.close()
		#self.meizitu_collection = db['meizitu'] ##在meizixiezhenji这个数据库中，选择一个集合
		self.title = '' ##用来保存页面主题
		self.url = '' ##用来保存页面地址
		self.img_urls = [] ##初始化一个 列表 用来保存图片地址

	def all_url(self, url):
		html = request.get(url,3)##调用request函数把套图地址传进去会返回给我们一个response
		Soup = BeautifulSoup(html.text, 'lxml')
		all_a = Soup.find('ul', id ='pins').find_all('a')  ##意思是先查找id为 pins 的ul标签，然后查找所有的<a>标签。
		
		a1 = all_a[1::2]
		for a in a1:
			title = a.get_text()
			self.title = title
			print(u'开始保存：', title) ##加点提示不然太枯燥了
			path = str(title).replace("?", '_') ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
			self.mkdir(path) ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
			href = a['href']
			listh=list(href)
			listh2=listh[-5:]
			href1=''.join(listh2)
			print(href1)

			self.url = href1 ##将页面地址保存到self.url中
			#print(self.url)
			href2 = (href1,)
			rs1 = self.find_one(href2)
			#self.find_one(href2)
			#self.html(href) ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦
			if rs1:
			#self.find_one(title.strip()):  ##判断这个主题是否已经在数据库中、不在就运行else下的内容，在则忽略。
				print(u'这个页面已经爬取过了')
			else:
				self.html(href)

	def html(self, href):   ##这个函数是处理套图地址获得图片的页面地址
		html = request.get(href, 3)
		max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
		page_num = 0
		for page in range(1, int(max_span) + 1):
			page_num = page_num + 1
			page_url = href + '/' + str(page)
			self.img(page_url, max_span, page_num) ##调用img函数

	def img(self, page_url, max_span, page_num): ##这个函数处理图片页面地址获得图片的实际地址
		img_html = request.get(page_url, 3)
		img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
		self.img_urls.append(img_url) ##每一次 for page in range(1, int(max_span) + 1)获取到的图片地址都会添加到 img_urls这个初始化的列表
		if int(max_span) == page_num: ##我们传递下来的两个参数用上了 当max_span和Page_num相等时，就是最后一张图片了，最后一次下载图片并保存到数据库中。
			self.save(img_url)
			post = (self.url, self.title, img_url, datetime.datetime.now())
			#print(post)
			self.insert(post)
		else:
			self.save(img_url)

	def select(self, args):
		conn = mysql.connector.connect(user='root', password='123456', database='test')
		cursor = conn.cursor()
		cursor.execute('select * from pachong where id = %s',args or ())
		values = cursor.fetchall()
		print(values)
	# 关闭Cursor和Connection:
		cursor.close()
		conn.close()
		return values

	def find_one(self,pk):
		rs = self.select(pk)
		return rs
	def insert(self,args):
		conn = mysql.connector.connect(user='root', password='123456', database='test')
		cursor = conn.cursor()
		# 创建user表:
		#cursor.execute('create table user2 (id varchar(20) primary key, name varchar(20))')
		# 插入一行记录，注意MySQL的占位符是%s:
		cursor.execute('insert into pachong (id, name, addr, time) values (%s, %s, %s, %s)', args)
		print('rowcount =', cursor.rowcount)
		# 提交事务:
		conn.commit()
		cursor.close()

	def save(self, img_url): ##这个函数保存图片
		name = img_url[-9:-4]
		img = request.get(img_url, 3)
		f = open(name + '.jpg', 'ab')
		f.write(img.content)
		f.close()

	def mkdir(self, path): ##这个函数创建文件夹
		path = path.strip()
		isExists = os.path.exists(os.path.join("D:\mzitu", path))
		if not isExists:
			print(u'建了一个名字叫做', path, u'的文件夹！')
			os.makedirs(os.path.join("D:\mzitu", path))
			os.chdir(os.path.join("D:\mzitu", path)) ##切换到目录
			return True
		else:
			print(u'名字叫做', path, u'的文件夹已经存在了！')
			return False
   
Mzitu = mzitu() ##实例化
Mzitu.all_url('http://www.mzitu.com') ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
