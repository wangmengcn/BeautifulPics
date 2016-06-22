# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
headers = {
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()


def get_url(start, end):
    num = 0
    head = start
    while head > end:
        url = "http://jandan.net/ooxx/page-" + str(head) + "#comments"
        print str(head)
        try:
            page = session.get(url).text
            pagesoup = BeautifulSoup(page.encode('utf-8'), 'html5lib')
            lis = pagesoup.select(".view_img_link")
            if lis != None:
                for item in lis:
                    picurl = item['href'].encode('utf-8')
                    print picurl
                    r = session.get(picurl, headers=headers)
                    with open("./pics/" + str(num) + '.jpg', 'wb') as f:
                        f.write(r.content)
                        f.close()
                        num += 1
                        time.sleep(3)
        except:
            print "出错了"
        time.sleep(10)
        head = head - 1

get_url(1699, 1650)
