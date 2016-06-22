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
refer = 'http://interfacelift.com//wallpaper/7yz4ma1/04020_jetincarina_1440x900.jpg'
acceot = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
uir = '1'
host = 'interfacelift.com'
connection = 'keep-alive'
pragma = 'no-cache'
acencode = 'gzip, deflate, sdch'
acln = 'en,zh-CN;q=0.8,zh;q=0.6'
headers = {
    'User-Agent': agent
    #'Referer':refer
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
            floder = 0
            for link in links:
                try:
                    taglink = link['href']
                    taglink = baseurl + taglink
                    tagname = link.next_element.encode('utf-8')
                    filepath = os.getcwd() + '/wallpaper/' + str(floder)
                    print taglink
                    print filepath
                    print os.path.exists(filepath)
                    if not os.path.exists(filepath):
                        os.mkdir(filepath)
                        floder += 1
                        linkend = 1
                        picinit = taglink + "index" + str(linkend) + ".html"
                        while download(picinit, filepath):
                            linkend += 1
                            picinit = taglink + "index" + \
                                str(linkend) + ".html"

                    else:
                        floder += 1
                        continue
                except:
                    floder += 1
                    print "下载出错"
        except Exception, e:
            print "出错了"


def download(picurl, path):

    delchar = ['%2C', '%27']
    if picurl:
        unique = Set()
        picpage = session.get(picurl).text
        picsoup = BeautifulSoup(picpage.encode('utf-8'), 'html5lib')
        divsoup = picsoup.select('a[href^="/wallpaper/details"]')
        if divsoup:
            try:
                split = 0
                for li in divsoup:
                    if split % 4 == 0:
                        baseurl = li['href'].split('/', -1)
                        id = int(baseurl[3])
                        subbase = baseurl[4].split('.', -1)
                        cleanbase = subbase[0].replace('_', '')
                        if '%2C' in cleanbase or '%27' in cleanbase:
                            cleanbase = cleanbase.replace('%2C', '')
                            cleanbase = cleanbase.replace('%27', '')
                        downloadurl = get_picurl(cleanbase, id, foo='1440x900')
                        print downloadurl, "--->", path
                        print cleanbase
                        get_file(downloadurl, cleanbase, path)
                    split += 1
                return True
            except:
                print "获取链接失败"
                return False
        else:
            return False
    else:
        return False


def get_picurl(base=None, id=None, foo='1440x900'):
    baseurl = "http://interfacelift.com"
    if base and id:
        suburl = "/wallpaper/7yz4ma1/" + \
            str(id) + '_' + base + '_' + foo + '.jpg'
        picurl = baseurl + suburl
        return picurl


def get_file(url, filename, path):
    if url:
        r = session.get(url, headers=headers)
        # print r.text.encode('utf-8')
        print filename
        picname = path + "/" + filename + '.jpg'
        with open(picname, 'wb') as f:
            f.write(r.content)
            print picname, "完成下载"
            # f.close()
        time.sleep(3)


# get_tags()
# get_file("http://interfacelift.com/wallpaper/7yz4ma1/01178_chicagoatnight_1440x900.jpg",'adas','.')

def test():
    get_tags()

test()
