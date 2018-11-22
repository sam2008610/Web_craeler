# html_doc = """
# <html>
# 	<head>
# 		<title>我是網頁標題</title>
# 		<style>
# 		.large {
# 	  	color:blue;
# 	  	text-align: center;
# 		}
# 		</style>
#   	</head>
#   	<body>
# 		<h1 class="large">我是變色且置中的抬頭</h1>
# 		<p id="p1">我是段落一</p>
# 		<p id="p2" style="">我是段落二</p>
# 		<p id="p3" style="">我是段落二</p>
# 		<div><a href='http://blog.castman.net' style="font-size:200%;">我是放大的超連結</a></div>
#   	</body>
# </html>
# """

# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html_doc,'html.parser')

# print(soup.find('p'))
# soup.find('p', id='p2')   # 回傳第一個被 <p> </p> 所包圍的區塊且 id="p2"
# soup.find(id='p2')        # 回傳第一個 id="p2" 的區塊
# soup.find_all('p')        # 回傳所有被 <p> </p> 所包圍的區塊
# soup.find('h1', 'large')  # 找尋第一個 <h1> 區塊且 class="large"

# pa = soup.find_all('p')
# for p in pa :
# 	  print(p['id'],p.text)
# a = soup.find('a')
# print(a['href'], a['style'], a.text)
# print(soup.find('h1')['class'])  # class 可以有多個值，故回傳 list
from bs4 import BeautifulSoup
import requests
import time
import os
import re
import urllib.request
import json


def get_articles(dom, date):
	soup = BeautifulSoup(dom, 'html.parser')

	articles = []
	divs = soup.find_all('div', 'r-ent')
	for d in divs:
		if d.find('div', 'date').string.strip() == date:  # 注意strip可清除前後空格
			push_count = 0
			if d.find('div', 'nrec').string:
				try:
					push_count = int(d.find('div', 'nrec').string)
				except ValueError:
					pass
			if d.find('a'):  # 有超連結，表示文章存在，未被刪除

				href = d.find('a')['href']
				title = d.find('a').string
				articles.append({
					'title': title,
					'href': href,
					'push_count': push_count
				})
	return articles


def get_web_page(url):
    time.sleep(0.5)  # 每次爬取前暫停 0.5 秒以免被 PTT 網站判定為大量惡意爬取
 	resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:  # statu_code取得 server 回覆的狀態碼 200 表示正常, 404 表示找不到網頁等
        print('Invalid url:', resp.url)
        return None
    else:
		return resp.text


def parse(dom):
    soup = BeautifulSoup(dom, 'html.parser')
	links = soup.find(id='main-cotent').find_all('a')
	img_urls = []
	for link in links:
		if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):  # ptt 有其他格式
    		img_urls.append(link['href'])
	return img_urls


def save(img_urls, title):
    if img_urls:
    	try:
			dname = title.strip()
			os.makedirs(dname)
			for img_url in img_urls:
    			if img_url.split('//')[1].startswith('m.'):
					img_url = img_url.replace('//m.', '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                	img_url = img_url.split('//')[0] + '//i.' + img_url.split('//')[1]
                if not img_url.endswith('.jpg'):
                    img_url += '.jpg'
                fname = img_url.split('/')[-1]
                urllib.request.urlretrieve(img_url, os.path.join(dname, fname))
        except Exception as e:
			print(e)
page = get_web_page(PTT_URL + '/bbs/Beauty/index.html')
if page:
	date = time.strftime("%m/%d").lstrip('0')  # 今天日期, 去掉開頭的 '0' 以符合 PTT 網站格式
	# print(date)
	current_articles = get_articles(page, date)
	for post in current_articles:
		print(post)

PTT_URL = 'https://www.ptt.cc'
for article in current_articles:
	new_page = get_web_page(PTT_URL + article['href'])
	if page:
		img_urls = parse(page)
		save(img_urls,article['title'])
		article['num_image'] = len(img_urls)
