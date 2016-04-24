# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
from sets import Set
import re
import os
import cookielib

# 构造 Request headers
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'
refer = 'https://interfacelift.com/wallpaper/details/2433/arch_in_the_sky.html'
acceot = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
uir = '1'
host = 'interfacelift.com'
connection = 'keep-alive'
pragma ='no-cache'
acencode ='gzip, deflate, sdch'
acln ='en,zh-CN;q=0.8,zh;q=0.6'
headers = {
    'User-Agent': agent,
    'Host':host,
    'Connection':connection,
    'pragma':pragma,
    'Accept-Encoding':acencode,
    'Accept-Language':acln
}

# 使用登录cookie信息
session = requests.session()

def get_tags():
	url = "https://interfacelift.com/wallpaper/tags/"
	baseurl = "https://interfacelift.com"
	tags = session.get(url).text.encode('utf-8')
	tagsoup = BeautifulSoup(tags, 'html5lib')

	cloud = tagsoup.select('.cloud', _candidate_generator=None, limit=None)
	for item in cloud:
		try:
			links = item.select('a')
			print len(links)
			for link in links:
				try:
					taglink = link['href']
					taglink = baseurl+taglink
					tagname = link.next_element.encode('utf-8')
					filepath = os.getcwd()+ '/wallpaper/'+tagname
					print taglink
					print filepath
					print os.path.exists(filepath)
					if not os.path.exists(filepath):
						os.mkdir(filepath)
						linkend = 1
						print taglink+"index"+str(linkend)+".html"
						while download(taglink+"index"+str(linkend)+".html",filepath):
							linkend+=1
					else:
						continue
				except:
					print "下载出错"
		except Exception, e:
			print "出错了"
		



def download(picurl,path):
	
	delchar = ['%2C','%27']
	if picurl:
		unique = Set()
		picpage = session.get(picurl).text
		picsoup = BeautifulSoup(picpage.encode('utf-8'), 'html5lib')
		divsoup = picsoup.select('a[href^="/wallpaper/details"]')
		if divsoup:
			try:
				split = 0
				for li in divsoup:
					if split%4==0:
						baseurl = li['href'].split('/',-1)
						id = int(baseurl[3])
						subbase = baseurl[4].split('.',-1)
						cleanbase = subbase[0].replace('_','')
						if '%2C' in cleanbase or '%27' in cleanbase:
							cleanbase = cleanbase.replace('%2C','')
							cleanbase = cleanbase.replace('%27','')
						downloadurl = get_picurl(cleanbase, id, foo='1440x900')
						print downloadurl
						get_file(downloadurl, cleanbase,path)
					split+=1
				return True
			except:
				print "获取链接失败"
				return False
		else:
			return False
	else:
		return False



def get_picurl(base=None,id=None,foo='1440x900'):
	baseurl = "https://interfacelift.com"
	if base and id :
		suburl = "/wallpaper/7yz4ma1/"+str(id)+'_'+base+'_'+foo+'.jpg'
		picurl = baseurl+suburl
		return picurl

def get_file(url,filename,path):
	if url:
		r = session.get(url, headers=headers,allow_redirects=False)
		print r.text.encode('utf-8')
		print path+"/"+filename+'.jpg'
		try:
			
			with open(path+"/"+filename+'.jpg', 'wb') as f:
				f.write(r.content)
				f.close()
				time.sleep(3)
		except :
			print "文件保存出错"
		


#download("https://interfacelift.com/wallpaper/tags/119/location/new_zealand/index20.html")
#get_tags()

get_file("https://interfacelift.com/wallpaper/D0464801/02433_archinthesky_1440x900.jpg", "abc", ".")



